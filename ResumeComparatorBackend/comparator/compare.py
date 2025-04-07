from api.job_posting.job_posting import JobPosting
from api.models.compare_report_model import CompareReport
from comparator.compare_utils.detail_generator import generate_detail
from comparator.compare_utils.stage_enum import Stage
from comparator.compare_utils.ai_tools.skill_extractor import extract_skills
from comparator.resume.resume import Resume
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from comparator.compare_utils.text_tools.pd_extractor import get_applicant_details
from comparator.stages.stage_1 import ai_raw_compare

"""
Compare class

This class represents a comparison between a resume and a job posting.
It will be provided with a resume and a job posting, and will 
compare the two.

Attributes:

    resume_path (str): The path to the resume file.
    job_posting_id (int): The id of the job posting.
    resume (Resume): A Resume object representing the resume.
    job_posting (JobPosting): A JobPosting object representing the job posting.
    resume_keywords (dict): A dictionary containing the extracted keywords from the resume.
    job_keywords (dict): A dictionary containing the extracted keywords from the job posting.
    
@Author: IFD
@Date: 2025-03-05
"""
class Compare:

    # Constructor
    def __init__(self, job_posting_id: int, resume_path: str):
        self.resume_path = resume_path
        self.job_posting_id = job_posting_id
        self.resume = Resume(self.resume_path)
        self.job_posting = JobPosting().create_from_json(job_posting_id=1)
        self.resume_keywords = extract_skills(self.resume.resume_text)
        self.job_keywords = extract_skills(self.job_posting.__str__())

    def compare_and_gen_report(self) -> CompareReport:
        """
        Compare the resume to the job posting.

        This method will fetch the job posting from the database and compare it to the resume.
        It will then calculate a score based on the comparison.

        Returns:
            CompareReport: A CompareReport instance containing the comparison results.
        """

        # Variables to store the score, applicant name, and applicant email
        score = 0
        applicant_name = get_applicant_details(self.resume.resume_text)['name']
        applicant_email = get_applicant_details(self.resume.resume_text)['email']

        # Get the score from the AI model (Stage 1)

        stage_one_score = ai_raw_compare(self.resume.resume_path, self.job_posting)

        if stage_one_score >= 55:

            passing_list = [generate_detail(Stage.STAGE_1, "Resume passed initial AI screening.")]

        else:

            failing_list = [generate_detail(Stage.STAGE_1, "Resume did not pass initial AI screening.")]

        # Get the keywords score (Stage 2)




        # Return a CompareReport instance with the score
        return CompareReport(resume=self.resume_path, job_id=self.job_posting_id,
                             applicant_name=applicant_name, applicant_email=applicant_email,
                             score=self.cosine_similarity_score())


    def cosine_similarity_score(self):
        """
        Compute the cosine similarity score between the resume and the job posting.

        Note that this is a first iteration. Much more enhanced methods will need
        to be used for a production-ready system.

        It currently only uses the SKILLS category for comparison.

        Returns:
            float: The cosine similarity score between the resume and the job posting.

        @Author: IFD
        @Date: 2025-03-17
        """

        nlp = spacy.load("en_core_web_sm")
        # Initialize scores dictionary
        scores = {}

        for category in self.job_keywords:
            # Only compare categories that are present in both job and resume
            if category in self.resume_keywords:
                resume_list = list(self.resume_keywords[category])
                job_list = list(self.job_keywords[category])

                # Convert keywords to vectors
                resume_vectors = [nlp(word).vector for word in resume_list if nlp(word).has_vector]
                job_vectors = [nlp(word).vector for word in job_list if nlp(word).has_vector]

                # Skip category if no vectors are found
                if not resume_vectors or not job_vectors:
                    scores[category] = 0.0
                    continue

                # Compute pairwise cosine similarities
                similarity_matrix = cosine_similarity(np.array(resume_vectors), np.array(job_vectors))

                # Take the maximum similarity for each job keyword
                max_similarities = similarity_matrix.max(axis=0)

                # Compute overall category similarity score
                scores[category] = round(max_similarities.mean(), 2) if len(max_similarities) > 0 else 0.0

        # Final score is just the skills score
        final_score = scores.get("SKILLS", 0)

        return round(final_score, 2)