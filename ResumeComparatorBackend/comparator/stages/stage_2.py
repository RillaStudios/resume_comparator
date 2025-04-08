import os

import django
from api.job_posting.job_posting import JobPosting
from comparator.compare_utils.ai_tools.cosine_similarity import compute_cosine_similarity
from comparator.compare_utils.ai_tools.skill_extractor import extract_skills, get_raw_skills
from comparator.compare_utils.text_tools.skill_matcher import skill_matcher
from comparator.resume.resume import Resume

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')

django.setup()

from django.conf import settings
BASE_DIR = settings.BASE_DIR

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

    # Extract skills
    skills_jp = extract_skills(job_text)
    skills_cv = extract_skills(resume_text)

    # Initialize plain text lists for hard and soft skills
    skills_jp_hard_list = get_raw_skills(skills_jp, False)
    skills_cv_hard_list = get_raw_skills(skills_cv, False)

    skills_jp_soft_list = get_raw_skills(skills_jp, True)
    skills_cv_soft_list = get_raw_skills(skills_cv, True)

    # Initialize scoring variables
    hard_skill_similarity = compute_cosine_similarity(skills_jp_hard_list, skills_cv_hard_list)
    soft_skill_similarity = compute_cosine_similarity(skills_jp_soft_list, skills_cv_soft_list)

    matches = skill_matcher(jp_hard_skills=skills_jp_hard_list, jp_soft_skills=skills_jp_soft_list,
                            cv_hard_skills=skills_cv_hard_list, cv_soft_skills=skills_cv_soft_list)

    print(matches['matched_hard_skills'])

    print("Matching Score: ", matches['match_score'])

    # FACTOR 1: Similarity score as base score
    base_score = (0.2 * hard_skill_similarity) + (0.1 * soft_skill_similarity) + (0.7 * matches['match_score'])

    # Final weighted score formula

    # Ensure score is between 0 and 1, then convert to percentage
    final_score = max(0, min(1, base_score)) * 100

    print(final_score)

    result = {

    }

    print(result)

    return result


resume_path = BASE_DIR / 'media' / 'resumes' / '77439230.pdf'
resume = Resume(str(resume_path))

print(keyword_similarity_score(1, resume.resume_text))
