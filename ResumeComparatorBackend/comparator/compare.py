from api.job_posting.job_posting import JobPosting
from api.models.compare_report_model import CompareReport
from comparator.resume.extraction_tools.keyword_extractor import extract_keywords
from comparator.resume.resume import Resume
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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
        self.resume_keywords = extract_keywords(self.resume.resume_text, target_labels=["SKILLS"])
        self.job_keywords = extract_keywords(self.job_posting.__str__(), target_labels=["SKILLS"])

    def compare_and_gen_report(self) -> CompareReport:
        """
        Compare the resume to the job posting.

        This method will fetch the job posting from the database and compare it to the resume.
        It will then calculate a score based on the comparison.

        Returns:
            CompareReport: A CompareReport instance containing the comparison results.
        """

        # Return a CompareReport instance with the score
        return CompareReport(resume=self.resume_path, job_id=self.job_posting_id, score=self.cosine_similarity_score())


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