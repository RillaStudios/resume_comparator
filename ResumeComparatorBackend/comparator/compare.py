from api.models.job_posting_model import JobPosting
import spacy
from sklearn.preprocessing import MinMaxScaler
import numpy as np


"""
Compare class

This class represents a comparison between a resume and a job posting.
It will fetch the job posting from the database via the job_posting_id.
It will then collect the Base64 encoded resume and compare it to the job posting.
Note that the resume is not stored in the database, it will be passed by the 
client as a Base64 encoded string.

Attributes:

    resume (str): The Base64 encoded resume.
    job_posting_id (int): The id of the job posting.
    passed (BooleanField): Whether the comparison passed.
    score (FloatField): The score of the comparison.
"""
class Compare:

    def __init__(self, job_posting_id: int, resume: str):
        self.resume = resume
        self.job_posting_id = job_posting_id
        self.passed = False
        self.score = 0.0
        self.nlp = spacy.load("en_core_web_md")

    def __str__(self):
        return self

    """
    Compare the resume to the job posting.
    
    This method will fetch the job posting from the database and compare it to the resume.
    It will then calculate a score based on the comparison.
    
    Returns:
        float: The score of the comparison.
    """
    def compare(self):
        job_posting = JobPosting.objects.get(id=self.job_posting_id)
        resume = self.resume

        # Tokenize the resume
        resume_doc = self.nlp(resume)
        job_doc = self.nlp(job_posting.description)

        similarity = resume_doc.similarity(job_doc)

        # Use a keyword-based scoring system
        keywords = self.extract_keywords(job_posting.description)
        matched_keywords = self.match_keywords(resume, keywords)

        print(f"Matched Keywords: {matched_keywords.conjugate()}")
        print("Keywords: ", keywords)

        # Calculate final score: Weighted sum of similarity and keyword match
        self.score = self.calculate_score(similarity, matched_keywords, keywords)

        # Set passed based on threshold
        if self.score > 50:  # Arbitrary threshold for passing
            self.passed = True
        else:
            self.passed = False

        # Compare the resume to the job posting
        # Calculate the score
        self.passed = True
        self.score = 0.0
        return self

    def extract_keywords(self, job_description: str):
        """
        Extract relevant keywords (skills, tools, technologies) from the job description.
        This could be improved by using NLP techniques or predefined lists.
        """
        # Simple approach: Extract words based on length and common sense.
        # You could expand this to be more sophisticated (e.g., using named entity recognition)
        job_doc = self.nlp(job_description)
        keywords = [token.text.lower() for token in job_doc if len(token.text) > 3 and not token.is_stop]
        return keywords

    def match_keywords(self, resume: str, keywords: list):
        """
        Compare the resume against the keywords extracted from the job description.
        Count how many keywords appear in the resume.
        """
        resume_doc = self.nlp(resume)
        matched_keywords = 0
        for keyword in keywords:
            if any([keyword in token.text.lower() for token in resume_doc]):
                matched_keywords += 1
        return matched_keywords

    def calculate_score(self, similarity, matched_keywords, keywords):
        """
        Calculate the final score based on a weighted sum of similarity and keyword matches.
        """
        similarity_weight = 0.7  # Adjust weights as necessary
        keyword_weight = 0.3

        # Normalize the number of matched keywords to be between 0 and 1
        max_keywords = len(keywords)
        normalized_keywords = matched_keywords / max_keywords if max_keywords > 0 else 0

        # Final score calculation
        score = (similarity * similarity_weight) + (normalized_keywords * keyword_weight * 100)

        return score