import os
import django
from api.job_posting.job_posting import JobPosting
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from comparator.compare_utils.ai_tools.skill_extractor import extract_skills
from comparator.resume.resume import Resume

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')

django.setup()

from django.conf import settings
BASE_DIR = settings.BASE_DIR

def compute_cosine_similarity(set1, set2) -> float:
    """
    Compute cosine similarity between two sets of skills.
    """
    vectorizer = TfidfVectorizer()
    corpus = [" ".join(set1), " ".join(set2)]  # Convert sets to strings
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return float(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0])

def keyword_similarity_score(job_posting_id: int, resume_text: str):
    """
    Calculate similarity scores and track matches/mismatches for both hard and soft skills.
    Uses cosine similarity to compare the skills extracted from the resume and job posting.
    
    Args:
        job_posting_id (int): The ID of the job posting.
        resume_text (str): The text content of the resume.


    Returns:
        dict: Contains matched and unmatched skills, along with similarity scores.
    """
    job_posting = JobPosting().create_from_json(job_posting_id)
    job_text = ""

    if job_posting.job_requirements_must_have:
        job_text += ", ".join(str(item) for item in job_posting.job_requirements_must_have)

    if job_posting.job_requirements_nice_to_have:
        job_text += ", " + ", ".join(str(item) for item in job_posting.job_requirements_nice_to_have)

    if job_posting.job_responsibilities:
        job_text += ". " + (job_posting.job_responsibilities if isinstance(job_posting.job_responsibilities, str)
                            else ", ".join(job_posting.job_responsibilities))

    # Extract skills
    skills_jp = extract_skills(job_text)
    skills_cv = extract_skills(resume_text)

    # Separate Hard and Soft Skills
    skills_jp_hard = set(k.lower() for k in skills_jp if k != 'SOFT')
    skills_cv_hard = set(k.lower() for k in skills_cv if k != 'SOFT')

    # Extract soft skills safely
    soft_skills_cv = skills_cv.get('SOFT', {})
    soft_skills_jp = skills_jp.get('SOFT', {})

    # If soft skills are stored as a dictionary, extract values
    soft_skills_cv = set(soft_skills_cv.values()) if isinstance(soft_skills_cv, dict) else set(soft_skills_cv)
    soft_skills_jp = set(soft_skills_jp.values()) if isinstance(soft_skills_jp, dict) else set(soft_skills_jp)

    # Compute Cosine Similarity
    hard_skill_similarity = compute_cosine_similarity(skills_jp_hard, skills_cv_hard)
    soft_skill_similarity = compute_cosine_similarity(soft_skills_jp, soft_skills_cv)

    # Identify Matches and Mismatches
    matched_hard_skills = skills_jp_hard & skills_cv_hard
    unmatched_hard_skills = skills_jp_hard - skills_cv_hard

    matched_soft_skills = soft_skills_cv & soft_skills_jp
    unmatched_soft_skills = soft_skills_cv - soft_skills_jp

    # Weighted Final Score
    final_score = (0.7 * hard_skill_similarity) + (0.3 * soft_skill_similarity)

    result = {
        "hard_skill_similarity": round(hard_skill_similarity, 2),
        "soft_skill_similarity": round(soft_skill_similarity, 2),
        "final_score": round(final_score, 2),
        "matched_hard_skills": list(matched_hard_skills),
        "unmatched_hard_skills": list(unmatched_hard_skills),
        "matched_soft_skills": list(matched_soft_skills),
        "unmatched_soft_skills": list(unmatched_soft_skills),
    }

    print(result)

    return result

resume_path = BASE_DIR / 'media' / 'resumes' / 'Chef-resume-example-28_9MAWlGV.pdf'
resume = Resume(str(resume_path))

print(keyword_similarity_score(1, resume.resume_text))
