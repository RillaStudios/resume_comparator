"""
processor.py - Handles text extraction, cleaning, and processing of resumes.

This module includes:
- `ResumeProcessor`: Extracts, cleans, and analyzes resume content.
- Uses `Utils` from utilsProcessor.py for text extraction and NLP processing.

author: shobhitrajain
date: 2025-03-05
"""

import os
import logging
import numpy as np
import spacy
import re
from .utilsProcessor import Utils, CountFrequency
from sklearn.feature_extraction.text import TfidfVectorizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the spaCy NLP model once for efficiency
nlp = spacy.load("en_core_web_md")


class ResumeProcessor:
    """Handles text extraction, cleaning, and processing for resumes."""

    def __init__(self, file_path):
        """
        Initializes ResumeProcessor with the file path.

        :param file_path: The absolute path of the uploaded resume.
        """
        self.file_path = file_path
        logger.info(f"Processing file: {self.file_path}")

    def extract_text(self):
        """Extracts raw text from the uploaded resume using file processing utilities."""
        return Utils.extract_text(self.file_path)

    def clean_text(self, text):
        """Cleans extracted text by removing stopwords and performing NLP preprocessing."""
        return Utils.clean_text(text)

    @staticmethod
    def extract_sections(text):
        """Extracts predefined sections from the resume based on common headings."""
        sections = {}
        current_section = "General"
        sections[current_section] = []

        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Check if line matches a known resume section
            if any(re.search(rf"\b{section}\b", line, re.IGNORECASE) for section in Utils.RESUME_SECTIONS):
                current_section = line.strip(":")  # Remove trailing colon if any
                sections[current_section] = []
            else:
                sections[current_section].append(line)

        # Remove empty sections and return structured output
        return {section: " ".join(content) for section, content in sections.items() if content}

    @staticmethod
    def extract_keywords(text, num_keywords=10):
        """Extracts top keywords from resume text using TF-IDF."""
        vectorizer = TfidfVectorizer(stop_words='english', max_features=50)
        tfidf_matrix = vectorizer.fit_transform([text])

        feature_array = np.array(vectorizer.get_feature_names_out())
        tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]

        top_keywords = feature_array[tfidf_sorting][:num_keywords]
        return list(top_keywords)

    @staticmethod
    def extract_contacts(text):
        """Extracts contact information such as emails, phone numbers, and links from text."""
        emails = re.findall(Utils.REGEX_PATTERNS["email_pattern"], text)
        links = re.findall(Utils.REGEX_PATTERNS["link_pattern"], text)
        phones = re.findall(Utils.REGEX_PATTERNS["phone_pattern"], text)

        return {
            "emails": emails if emails else "No email found",
            "links": links if links else "No links found",
            "phones": phones if phones else "No phone numbers found",
        }

    def count_word_frequency(self, text):
        """Counts the frequency of words in the processed text."""
        return CountFrequency(text).count_frequency()

    def process(self):
        """
        Executes the full pipeline for processing resumes.

        Steps:
        - Extract raw text
        - Clean text
        - Identify resume sections
        - Count word frequencies
        - Extract important keywords
        - Extract contact information

        :return: A structured dictionary with processed resume data.
        """
        try:
            logger.info(f"Starting processing for file: {self.file_path}")
            raw_text = self.extract_text()
            cleaned_text = self.clean_text(raw_text)
            sections = self.extract_sections(raw_text)
            word_frequency = self.count_word_frequency(cleaned_text)
            keywords = self.extract_keywords(cleaned_text)
            contacts = self.extract_contacts(raw_text)

            # Cleanup temp file
            os.remove(self.file_path)
            logger.info(f"Processing completed, temp file removed: {self.file_path}")

            return {
                "cleaned_text": cleaned_text,
                "sections": sections,
                "word_frequency": word_frequency,
                "keywords": keywords,
                "contacts": contacts
            }
        except Exception as e:
            logger.error(f"Error in processing resume: {str(e)}", exc_info=True)
            return {"error": str(e)}