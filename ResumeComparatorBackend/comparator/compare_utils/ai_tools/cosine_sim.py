from sentence_transformers import SentenceTransformer
from api.job_posting.job_posting import JobPosting
from comparator.compare_utils.ai_tools.pdf_parser import classify_text
from cleantext.sklearn import CleanTransformer

def skill_similarity(resume_text: str, job_posting_id: int = None) -> float:

    # Create a CleanTransformer object to clean the text
    cleaner = CleanTransformer(no_punct=False, lower=False)

    # Create the job posting object
    job_posting = JobPosting().create_from_json(job_posting_id)

    # Extract skills section from the resume
    sections = classify_text(resume_text)

    # Clean the skills section
    skills = cleaner.transform([sections['skills']])[0]

    # Extract job requirements
    return __model_sim_score(job_posting.job_requirements_must_have, skills)


def __model_sim_score(req_list: list[str], skills: str):

    # Load the pre-trained SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    if req_list is not None:
        job_skills = ", ".join(str(item) for item in req_list)

        compare_skills = [skills, job_skills]

        # Calculate cosine similarity
        embeddings = model.encode(compare_skills)

        similarities = model.similarity(embeddings, embeddings)

        # Extract the similarity between resume skills and job skills (value at position [0,1])
        similarity_score = similarities[0, 1].item()  # Convert tensor value to Python float
        similarity_percentage = similarity_score * 100

        return similarity_percentage