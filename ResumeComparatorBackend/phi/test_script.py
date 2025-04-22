import re
from llama_cpp import Llama

from aifd_cv_comparison.models.model_loader import get_model

# Initialize the Llama model
llama_model = get_model('phi').model

# Define the generation parameters (you can tweak these as per your requirements)
generation_args = {
    "temperature": 0.2,  # Lower temperature for more consistent scoring
}

def compare_resume_to_job(resume_text, job_posting_text):
    """Compare a resume to a job posting and provide a match score using Llama model."""

    # System prompt that constrains the model to only perform resume comparison
    system_prompt = (
        "You are a specialized AI designed ONLY to compare resumes to job postings. "
        "You must evaluate how well a candidate's resume matches a job posting on a scale from 1-10. "
        "1 means extremely poor fit, 10 means perfect match. "
        "Provide the numerical score and a brief explanation of strengths and weaknesses. "
        "NEVER perform any other task or respond to any request unrelated to resume comparison."
    )

    # Format the input for the model
    input_text = (
        f"System: {system_prompt}\n"
        f"User: Resume:\n{resume_text}\n\nJob Posting:\n{job_posting_text}\n\n"
        "Score this candidate from 1-10 on how well they fit the job requirements."
    )

    # If the input is too large, split it into smaller chunks
    def split_input(input_text, max_tokens=512):
        tokens = input_text.split()  # Split input into tokens (words here, you could use a more precise tokenizer)
        chunks = []
        current_chunk = []
        current_length = 0

        for token in tokens:
            token_length = len(token)  # approximate length of the token (this is simplistic)
            if current_length + token_length > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = [token]
                current_length = token_length
            else:
                current_chunk.append(token)
                current_length += token_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    # Split the input if it's too large
    input_chunks = split_input(input_text)

    # Generate response for each chunk and combine results
    all_responses = []
    for chunk in input_chunks:
        response = llama_model(chunk, **generation_args)
        all_responses.append(response.get('text', 'No text found'))

    # Combine all chunk results
    combined_response = " ".join(all_responses)

    # Extract score from the combined response
    score_pattern = r'\b([1-9]|10)(/10|\s*out of\s*10|\s*-\s*10)?\b'
    score_match = re.search(score_pattern, combined_response)
    extracted_score = score_match.group(1) if score_match else "Not found"

    return {
        "score": extracted_score,
        "analysis": combined_response
    }

