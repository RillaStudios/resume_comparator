from pathlib import Path

import torch
from django.conf import settings
from sentence_transformers import CrossEncoder

from api.job_posting.job_posting import JobPosting
from api.models.compare_report_model import CompareReport
from comparator.resume.resume import Resume

"""
Compare class

This class represents a comparison between a resume and a job posting.
It will be provided with a resume and a job posting, and will 
compare the two.

Attributes:

    resume (str): The Base64 encoded resume.
    job_posting_id (int): The id of the job posting.
    
@Author: IFD
@Date: 2025-03-05
"""
class Compare:

    # Constructor
    def __init__(self, job_posting_id: int, resume_path: str):
        self.resume_path = resume_path
        self.job_posting_id = job_posting_id

    """
    Compare the resume to the job posting.
    
    This method will fetch the job posting from the database and compare it to the resume.
    It will then calculate a score based on the comparison.
    
    Returns:
        float: The score of the comparison.
    """

    def compare_and_gen_report(self) -> CompareReport:
        model_path = Path(settings.BASE_DIR, 'ai_models', 'ms-marco-MiniLM-L6-v2')
        model = CrossEncoder(str(model_path))

        resume = Resume(self.resume_path)
        job_posting = JobPosting().create_from_json(job_posting_id=1)

        # Combine all job requirements into a single string
        job_requirements_str = " ".join(job_posting.job_requirements_must_have).join(job_posting.job_requirements_nice_to_have)

        print(resume.skills)

        # Print raw logits before applying sigmoid
        skills_score_raw = model.predict([(resume.skills, job_requirements_str)])[0]
        experience_score_raw = model.predict([(resume.experience, job_requirements_str)])[0]
        education_score_raw = model.predict([(resume.education, job_requirements_str)])[0]
        summary_score_raw = model.predict([(resume.summary, job_posting.job_summary)])[0]

        final_score = (skills_score_raw * 0.8) + (experience_score_raw * 0.5) + (education_score_raw * 0.4) + (
                    summary_score_raw * 0.15)

        print(f"Final Score: {final_score}")

        # Return a CompareReport instance with the score
        return CompareReport(resume=self.resume_path, job_id=self.job_posting_id, score=final_score)

def normalize_logit(logit, min_val, max_val):
    # Scale the logit to be between 0 and 1
    return (logit - min_val) / (max_val - min_val)