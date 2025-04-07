import numpy as np
from gensim.models import Doc2Vec
from numpy.linalg import norm

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

    ai_path = "../../ai_models/cv_job_maching.model"

    try:
        model = Doc2Vec.load(ai_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return 0

    resume_text = extract_text_from_pdf(resume_path)
    job_posting_text = JobPosting().create_from_json(job_posting_id).get_text()

    v1 = model.infer_vector(resume_text.split())  # Vector for resume
    v2 = model.infer_vector(job_posting_text.split())  # Vector for job posting

    if norm(v1) == 0 or norm(v2) == 0:
        print("One of the vectors is zero, cannot compute similarity.")
        return 0

    similarity = 100 * (np.dot(v1, v2) / (norm(v1) * norm(v2)))

    return similarity