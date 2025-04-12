from pathlib import Path
from aifd_cv_comparison.models import load_models
from aifd_cv_comparison.resume_process.section_classifier.resume_classifier import classify_resume
from aifd_cv_comparison.utils.extract_text_from_pdf import extract_text_from_pdf
from aifd_cv_comparison.utils.resume import Resume


def process_resume(resume: str | Path):

    load_models()

    # Check if the resume is a file path or text
    if isinstance(resume, Path):  # Changed from "resume is Path"
        # Extract text from the PDF file
        resume_text = extract_text_from_pdf(str(resume))
    else:
        # If it's a string, use it as is
        resume_text = resume

    # Initialize the Resume object
    resume = Resume(
        raw_text=resume_text,
    )

    #Classify the resume text into sections
    classify_resume(resume)

    # Check if the resume is in a valid format (this is determined by the classifier)
    if resume.bad_format:
        print("The resume is not in a valid format.")
        return

    # Print the classified sections
    print(resume.experience)

process_resume(Path('../../tests/resumes/Java-Developer-Resume-4_IXHdxCI.pdf'))

