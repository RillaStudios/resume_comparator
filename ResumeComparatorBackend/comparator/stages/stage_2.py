import os

import django
from api.job_posting.job_posting import JobPosting
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

    Returns:
        dict: Contains matched and unmatched skills, along with a smart similarity score.
    """
    job_posting = JobPosting().create_from_json(job_posting_id)
    job_text = ""

    if job_posting.job_requirements_must_have:
        job_text += ", ".join(str(item) for item in job_posting.job_requirements_must_have)

    # Extract skills
    skills_jp = extract_skills(job_text)
    skills_cv = extract_skills(resume_text)

    # Separate into hard/soft skills
    skills_jp_hard_list = get_raw_skills(skills_jp, False)
    skills_cv_hard_list = get_raw_skills(skills_cv, False)
    skills_jp_soft_list = get_raw_skills(skills_jp, True)
    skills_cv_soft_list = get_raw_skills(skills_cv, True)

    # Get matching results
    matches = skill_matcher(
        jp_hard_skills=skills_jp_hard_list,
        jp_soft_skills=skills_jp_soft_list,
        cv_hard_skills=skills_cv_hard_list,
        cv_soft_skills=skills_cv_soft_list
    )

    # Calculate weights
    total_possible = (
        len(skills_jp_hard_list) * 2 +
        len(skills_jp_soft_list)
    )

    actual_score = (
        len(matches["matched_hard_skills"]) * 2 +
        len(matches["matched_soft_skills"])
    )

    # Bonus points
    bonus = 0
    bonus += len(matches["extra_hard_skills"]) * 0.5  # extra hard skills
    bonus += len(matches["extra_soft_skills"]) * 0.25  # extra soft skills

    # Normalize score
    raw_score = actual_score + bonus
    final_score = min((raw_score / total_possible) * 100, 100)

    result = {
        "score": round(final_score, 2),
        "matched_hard_skills": matches["matched_hard_skills"],
        "unmatched_hard_skills": matches["unmatched_hard_skills"],
        "extra_hard_skills": matches["extra_hard_skills"],
        "matched_soft_skills": matches["matched_soft_skills"],
        "unmatched_soft_skills": matches["unmatched_soft_skills"],
        "extra_soft_skills": matches["extra_soft_skills"],
    }

    print(result)  # Optional for debugging
    return result



resume_path = BASE_DIR / 'media' / 'resumes' / 'FordDow_Izaak_Resume_2025_QYj15fz_SNi9F5f.pdf'
resume = Resume(str(resume_path))

print(keyword_similarity_score(1, resume.resume_text))
