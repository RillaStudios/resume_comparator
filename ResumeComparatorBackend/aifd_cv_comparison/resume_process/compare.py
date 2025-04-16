import os
import django
from DjangoApp.settings import BASE_DIR

# Set up Django environment first - before any imports that use Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')
django.setup()

from pathlib import Path
from aifd_cv_comparison.models import load_models
from aifd_cv_comparison.resume_process.section_classifier.resume_classifier import classify_resume
from aifd_cv_comparison.config.compare_settings import CompareSettings, CompareSettingsType
from aifd_cv_comparison.utils.extract_text_from_pdf import extract_text_from_pdf
from aifd_cv_comparison.resume_process.comparisons.optimized import optimized_resume_comparison
from aifd_cv_comparison.utils.resume import Resume
from api.models import JobPosting

def compare_resumes(resumes: list[str | Path], job_posting_id: int, settings: CompareSettings) -> None:

    # Verify resumes is a list of strings or Path objects
    if not isinstance(resumes, list) or not all(isinstance(r, (str, Path)) for r in resumes):
        raise TypeError("Resumes must be a list of strings or Path objects")

    load_models()

    # Load the job posting
    try:
        job_posting = JobPosting.objects.get(id=job_posting_id)
    except JobPosting.DoesNotExist:
        raise ValueError(f"Job posting with ID {job_posting_id} does not exist.")

    for resume in resumes:

        # Check if the resume is a file path or text
        if isinstance(resume, Path) or (isinstance(resume, str) and os.path.isfile(resume)):

            # Extract text from the PDF file
            resume_text = extract_text_from_pdf(str(resume))
        else:

            # If it's a string, use it as is
            resume_text = resume

        # Initialize the Resume object
        resume = Resume(
            raw_text=resume_text,
        )

        #Classify the resume text into sections (this will be done no matter the setting)
        classify_resume(resume)

        # Check if the resume is in a valid format (this is determined by the classifier)
        #If the resume is not in a valid format, we will not process it further
        if resume.bad_format: return

        if settings.setting == CompareSettingsType.OPTIMIZED:
            #Simple doc2vec comparison
            # This is a placeholder for the optimized comparison logic
            score = optimized_resume_comparison(resume, job_posting)

            print(f"Comparison score: {score}")
        elif settings.setting == CompareSettingsType.BASIC:
            # Basic comparison logic
            # This is a placeholder for the basic comparison logic
            print('Basic comparison logic executed.')
        elif settings.setting == CompareSettingsType.ADVANCED:
            # Advanced comparison logic
            # This is a placeholder for the advanced comparison logic
            print('Advanced comparison logic executed.')
        else:
            raise ValueError("Invalid comparison setting. Choose from BASIC, OPTIMIZED, or ADVANCED.")

resume_path = os.path.join(BASE_DIR, "media", "resumes", "Java-Developer-Resume-4.pdf")

compare_resumes([resume_path], 1, CompareSettings(CompareSettingsType.OPTIMIZED, False))
