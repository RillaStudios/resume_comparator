import docx
import pdfplumber

"""
This module contains the Resume class which is used to 
extract text from a resume file.

Attributes:
    resume_path (str): The path to the resume file.
    
@Author: IFD
@Date: 2025-03-05
"""
class Resume:

    # Constructor
    def __init__(self, resume_path):
        self.resume_path = resume_path

    # Extract text from a PDF file
    def __extract_text_from_pdf(self) -> str:
        text = ""
        with pdfplumber.open(self.resume_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    # Extract text from a DOCX file
    def __extract_text_from_docx(self) -> str:
        doc = docx.Document(self.resume_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    # Extract text from the resume file
    def extract_text(self) -> str:
        if self.resume_path.endswith(".pdf"):
            return self.__extract_text_from_pdf()
        elif self.resume_path.endswith(".docx"):
            return self.__extract_text_from_docx()
        else:
            raise ValueError("Unsupported file format. Use PDF or DOCX.")