import pymupdf as fitz
from cleantext.sklearn import CleanTransformer
"""
A utility function to extract raw text from a PDF file.

@Author: IFD
@Since: 2025-04-01
"""
def extract_text_from_pdf(file_path):
    """
    Extracts raw text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted raw text.
    """
    # Create a CleanTransformer object to clean the text
    cleaner = CleanTransformer(no_punct=False, lower=False)

    # Assign an empty string to store the extracted text
    text = ""

    # Open the resume file
    doc = fitz.open(file_path)

    # Extract text from each page
    for page in doc:
        text += page.get_text("text") + "\n"
    raw_text = text.strip()
    cleaned_text = cleaner.transform([raw_text])[0]
    return cleaned_text