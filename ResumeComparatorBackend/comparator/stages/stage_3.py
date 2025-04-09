import os
import django
from django.conf import settings
from sentence_transformers import SentenceTransformer, util
from api.job_posting.job_posting import JobPosting
from comparator.compare_utils.ai_tools.pdf_parser import classify_text
from comparator.resume.resume import Resume
from cleantext.sklearn import CleanTransformer

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')

django.setup()

def resume_fit(resume_text: str, job_posting_id: int = None):

    # Create a CleanTransformer object to clean the text
    cleaner = CleanTransformer(no_punct=False, lower=False)

    # Create the job posting object
    job_posting = JobPosting().create_from_json(1)

    # Extract skills section from the resume
    sections = classify_text(resume_text)

    # Clean the skills section
    skills = cleaner.transform([sections['skills']])[0]

    # Extract job requirements
    score = model_sim_score(job_posting.job_requirements_must_have, skills)

    print(score)

    e_score = model_sim_score(job_posting.job_requirements_nice_to_have, skills)

    final_score = ((score * 0.7) + (e_score * 0.3))

    print(final_score)

def model_sim_score(req_list: list[str], skills: str):

    # Load the pre-trained SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    if req_list is not None:
        job_skills = ", ".join(str(item) for item in req_list)

        compare_skills = [skills, job_skills]

        # Calculate cosine similarity
        embeddings = model.encode(compare_skills)

        similarities = model.similarity(embeddings, embeddings)

        # Extract the similarity between resume skills and job skills (value at position [0,1])
        similarity_score = similarities[0, 1].item()  # Convert tensor value to Python float
        similarity_percentage = similarity_score * 100

        return similarity_percentage

resume_path = os.path.join(settings.BASE_DIR, 'media', 'resumes', 'Michael Tettey_Tamatey_Resume..pdf')
resume = Resume(resume_path)
resume_text = resume.resume_text

resume_fit(resume_text)
