# """
# utilsProcessor.py - Utility functions for text extraction, cleaning, and keyword processing.
#
# Includes:
# - Text extraction from PDF/DOCX
# - Data cleaning and NLP processing
# - Keyword extraction using TF-IDF
#
# author: shobhitrajain
# date: 2025-03-05
# """
#
# import os
# import fitz  # PyMuPDF for PDFs
# import docx
# import spacy
# import re
#
# class Utils:
#     """Utility class for text extraction, cleaning, and processing."""
#
#     # Load spaCy model once for efficiency
#     nlp = spacy.load("en_core_web_md")
#
#     # Predefined regex patterns for extracting contact details
#     REGEX_PATTERNS = {
#         "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
#         "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
#         "link_pattern": r"\b(?:https?://|www\.)\S+\b",
#     }
#
#     # Common resume section headers
#     RESUME_SECTIONS = [
#         "Contact Information", "Objective", "Summary", "Education", "Experience",
#         "Skills", "Projects", "Certifications", "Licenses", "Awards", "Honors",
#         "Publications", "References", "Technical Skills", "Computer Skills",
#         "Programming Languages", "Software Skills", "Soft Skills", "Language Skills",
#         "Professional Skills", "Work Experience", "Employment History", "Internship Experience",
#     ]
#
#     @staticmethod
#     def extract_text(file_path):
#         """Extract text from a PDF or DOCX file."""
#         ext = os.path.splitext(file_path)[1].lower()
#
#         if ext == ".pdf":
#             return Utils.extract_text_from_pdf(file_path)
#         elif ext == ".docx":
#             return Utils.extract_text_from_docx(file_path)
#         else:
#             raise ValueError("Unsupported file format")
#
#     @staticmethod
#     def extract_text_from_pdf(pdf_path):
#         """Extract text from a PDF file using PyMuPDF."""
#         try:
#             text = ""
#             with fitz.open(pdf_path) as doc:
#                 for page in doc:
#                     text += page.get_text("text")
#             return text.strip()
#         except Exception as e:
#             return f"Error reading PDF: {str(e)}"
#
#     @staticmethod
#     def extract_text_from_docx(docx_path):
#         """Extract text from a DOCX file."""
#         try:
#             doc = docx.Document(docx_path)
#             return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
#         except Exception as e:
#             return f"Error reading DOCX: {str(e)}"
#
#     @staticmethod
#     def remove_emails_links(text):
#         """Remove emails, phone numbers, and links from text."""
#         for pattern in Utils.REGEX_PATTERNS.values():
#             text = re.sub(pattern, "", text)
#         return text
#
#     @staticmethod
#     def clean_text(text):
#         """Preprocess text by removing filler words and extracting key phrases."""
#         text = text.lower()
#         text = Utils.remove_emails_links(text)
#         doc = Utils.nlp(text)
#
#         important_words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
#         return " ".join(important_words)
#
#
# class CountFrequency:
#     """Class for counting word frequency in text using spaCy NLP."""
#
#     def __init__(self, text):
#         """
#         Initialize CountFrequency with text.
#
#         :param text: The processed resume text.
#         """
#         self.text = text
#         self.doc = Utils.nlp(text)  # Use the spaCy model from Utils
#
#     def count_frequency(self):
#         """
#         Count the frequency of different word types (e.g., nouns, verbs, adjectives).
#
#         :return: A dictionary containing part-of-speech frequencies.
#         """
#         pos_freq = {}
#         for token in self.doc:
#             if token.pos_ in pos_freq:
#                 pos_freq[token.pos_] += 1
#             else:
#                 pos_freq[token.pos_] = 1
#         return pos_freq
