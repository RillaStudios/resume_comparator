from api.models.report_model import Report

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
        self.resume = resume_path
        self.job_posting_id = job_posting_id

    """
    Compare the resume to the job posting.
    
    This method will fetch the job posting from the database and compare it to the resume.
    It will then calculate a score based on the comparison.
    
    Returns:
        float: The score of the comparison.
    """
    def compare_and_gen_report(self) -> Report:

        # job_posting = JobPosting.objects.get(id=self.job_posting_id)
        # resume = self.resume
        #
        # # Tokenize the resume
        # resume_doc = self.nlp(resume)
        # job_doc = self.nlp(job_posting.description)
        #
        # similarity = resume_doc.similarity(job_doc)
        #
        # # Use a keyword-based scoring system
        # keywords = self.extract_keywords(job_posting.description)
        # matched_keywords = self.match_keywords(resume, keywords)
        #
        # print(f"Matched Keywords: {matched_keywords.conjugate()}")
        # print("Keywords: ", keywords)
        #
        # # Calculate final score: Weighted sum of similarity and keyword match
        # self.score = self.calculate_score(similarity, matched_keywords, keywords)
        #
        # # Set passed based on threshold
        # if self.score > 50:  # Arbitrary threshold for passing
        #     self.passed = True
        # else:
        #     self.passed = False
        #
        # # Compare the resume to the job posting
        # # Calculate the score
        # self.passed = True
        # self.score = 0.0
        return self