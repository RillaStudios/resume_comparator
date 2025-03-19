from pathlib import Path
from django.conf import settings
from comparator.resume.extraction_tools.extract import extract_text
from comparator.resume.extraction_tools.section_classifier import classify_sections

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
        self.resume_text = extract_text(str(self.resume_path))
        self.sections = classify_sections(self.resume_text)
