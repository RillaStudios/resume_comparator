import fitz
from cleantext.sklearn import CleanTransformer

def extract_text(resume_path: str) -> str:
    """
    Extracts raw text from the resume file.

    Args:
        resume_path (str): The path to the resume file.

    Returns:
        str: The extracted raw text

    Author: IFD
    Date: 2025-03-17
    """

    # Create a CleanTransformer object to clean the text
    cleaner = CleanTransformer(no_punct=False, lower=False)

    # Assign an empty string to store the extracted text
    text = ""

    # Open the resume file
    doc = fitz.open(resume_path)

    # Extract text from each page
    for page in doc:
        text += page.get_text("text") + "\n"
    raw_text = text.strip()
    cleaned_text = cleaner.transform([raw_text])[0]
    return cleaned_text
