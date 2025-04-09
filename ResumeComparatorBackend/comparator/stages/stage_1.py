import os
import numpy as np
from gensim.models import Doc2Vec
from numpy.linalg import norm
from DjangoApp import settings
from api.job_posting.job_posting import JobPosting
from comparator.compare_utils.text_tools.extract_text_from_pdf import extract_text_from_pdf

"""
Stage 1 of comparing resumes to job postings:

Uses cv_job_maching.model to compare resumes to job postings. This model
gives an initial score and if the score is high enough, the resume is sent to
the next stage for further processing.

@Author: IFD
@Date: 2025-04-01
"""
def ai_raw_compare(resume_path: str, job_posting_id: int) -> float:
    """
    A function to compare a resume to a job posting using a Doc2Vec model.
    This provides an initial score for the comparison. It is used to determine
    if a resume should be sent to the next stage for further processing.
    (Raw comparison)

    Args:
        resume_path (str): The path to the resume file.
        job_posting_id (int): The id of the job posting.

    @Author: IFD
    @Since: 2025-04-01
    """


    model_path = os.path.join(settings.BASE_DIR, 'ai_models', 'cv_job_maching.model')
    resume_path = os.path.join(settings.BASE_DIR, 'media', resume_path)

    # Move this inside try block
    try:
        # Load the model
        model = Doc2Vec.load(model_path)

        # Get the job posting - this is where the error occurs
        job_posting = JobPosting().create_from_json(job_posting_id)
        job_posting_text = job_posting.get_text()

        resume_text = extract_text_from_pdf(resume_path)

        v1 = model.infer_vector(resume_text.split())  # Vector for resume
        v2 = model.infer_vector(job_posting_text.split())  # Vector for job posting

        if norm(v1) == 0 or norm(v2) == 0:
            print("One of the vectors is zero, cannot compute similarity.")
            return 0

        similarity = 100 * (np.dot(v1, v2) / (norm(v1) * norm(v2)))
        return similarity

    except ValueError as e:
        print(f"Error getting job posting: {e}")
        # Debug: List available job postings
        try:
            all_postings = JobPosting().create_from_json(job_posting_id=None)
            available_ids = [p['id'] for p in all_postings]
            print(f"Available job posting IDs: {available_ids}")
            # Also check the type of IDs
            print(f"ID types: {[type(p['id']) for p in all_postings]}")
        except Exception as inner_e:
            print(f"Error getting available job postings: {inner_e}")
        return 0
    except Exception as e:
        print(f"Error in ai_raw_compare: {e}")
        return 0
