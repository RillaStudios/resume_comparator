from aifd_cv_comparison.models import load_models
from aifd_cv_comparison.models.model_loader import get_model
from tests.text_utils import extract_text_from_pdf


def chunk_text(text, max_chunk_size=512, tokenizer=None):
    """Split text into chunks of approximately max_chunk_size tokens, with natural separation."""
    if not tokenizer:
        raise ValueError("A tokenizer must be provided to count tokens.")

    lines = text.split('\n')
    chunks, current_chunk, current_size = [], [], 0

    for line in lines:
        line_size = len(tokenizer.tokenize(line))

        if current_size + line_size > max_chunk_size:
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            current_chunk, current_size = [line], line_size
        else:
            current_chunk.append(line)
            current_size += line_size

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks or [text]



# load_models()
#
# tokenizer = get_model('resume_parser').tokenizer
#
# resume_text=extract_text_from_pdf.py(file_path="../../tests/resumes/Michael Tettey_Tamatey_Resume_nV4GIMR..pdf")
#
# chunks = chunk_text(resume_text, max_chunk_size=512, tokenizer=tokenizer)
#
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i+1}:\n{chunk}\n")