from pathlib import Path
from django.conf import settings

from comparator.compare_utils.ai_tools.pdf_parser import classify_text
from comparator.compare_utils.text_tools.extract_text_from_pdf import extract_text_from_pdf

"""
Resume class for extracting and classifying sections from resume documents.

Args:
    resume_path (str): The path to the resume file.
    resume_text (str): The raw text extracted from the resume file.
    sections (dict): A dictionary containing classified sections from the resume text.

Author: IFD
Date: 2025-03-17
"""
class Resume:

    def __init__(self, resume_path):
        self.resume_path = Path(settings.BASE_DIR) / 'media' / resume_path
        self.resume_text = extract_text_from_pdf(str(self.resume_path))
        self.sections = classify_text(self.resume_text)
