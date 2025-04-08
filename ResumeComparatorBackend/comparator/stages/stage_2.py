import os
from typing import Dict

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
    if not set1 or not set2:
        return 0.0  # No similarity if either set is empty

    vectorizer = TfidfVectorizer()
    corpus = [" ".join(set1), " ".join(set2)]  # Convert sets to strings
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return float(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0])

def get_raw_skills(raw_list: dict, soft: bool) -> list[str]:
    """
    A helper function to extract raw skills from the raw_list. Will also
    remove duplicates and convert them to lowercase.

    Args:
        raw_list (dict): The dictionary containing skills categorized as HARD or SOFT.
        soft (bool): If True, extract soft skills; if False, extract hard skills.

    Returns:
        list[str]: A list of skills (words) that match the criteria.

    @Author: IFD
    @Date: 2025-04-07
    """

    raw_skills = []

    for category, skills in raw_list.items():
        for skill in skills:
            skill_word = skill['word'].lower()
            if skill['score'] > 0.98:
                if (soft and category == 'SOFT') or (not soft and category != 'SOFT'):
                    # Check if the skill is already in the list
                    if skill_word not in raw_skills:
                        raw_skills.append(skill_word)

    return raw_skills

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

    # Initialize scoring variables
    hard_skill_similarity = 0.0
    soft_skill_similarity = 0.0
    matched_hard_skills = set()
    unmatched_hard_skills = set()
    matched_soft_skills = set()
    unmatched_soft_skills = set()
    bonus_hard_skills = set()
    bonus_soft_skills = set()
    final_score = 0.0

    # Initialize sets for Hard and Soft Skills
    skills_jp_hard_list = get_raw_skills(skills_jp, False)
    skills_cv_hard_list = get_raw_skills(skills_cv, False)

    skills_jp_soft_list = get_raw_skills(skills_jp, True)
    skills_cv_soft_list = get_raw_skills(skills_cv, True)

    if not skills_jp_soft_list:
        with_soft = False
    else:
        with_soft = True

    # Compute Cosine Similarity
    hard_skill_similarity = compute_cosine_similarity(skills_jp_hard_list, skills_cv_hard_list)
    soft_skill_similarity = compute_cosine_similarity(skills_jp_soft_list, skills_cv_soft_list) if with_soft else None

    # Identify Matches and Mismatches
    matched_hard_skills = set(skills_jp_hard_list) & set(skills_cv_hard_list)
    unmatched_hard_skills = set(skills_jp_hard_list) - set(skills_cv_hard_list)
    extra_hard_skills = set(skills_cv_hard_list) - set(skills_jp_hard_list)

    matched_soft_skills = set(skills_jp_soft_list) & set(skills_cv_soft_list)
    unmatched_soft_skills = set(skills_jp_soft_list) - set(skills_cv_soft_list)
    extra_soft_skills = set(skills_cv_soft_list) - set(skills_jp_soft_list)

    # FACTOR 1: Similarity score as base score
    base_score = (0.7 * hard_skill_similarity) + (0.3 * soft_skill_similarity)

    print("Base Score:", base_score)

    # FACTOR 2: Match rates
    hard_skill_match_rate = (
        len(matched_hard_skills) / len(skills_jp_hard_list) if skills_jp_hard_list else 0
    )

    print("Hard Skill Match Rate:", hard_skill_match_rate)

    soft_skill_match_rate = (
        len(matched_soft_skills) / len(skills_jp_soft_list) if skills_jp_soft_list else 0
    )

    print("Soft Skill Match Rate:", soft_skill_match_rate)

    match_rate_score = (0.7 * hard_skill_match_rate) + (0.3 * soft_skill_match_rate)

    print("Match Rate Score:", match_rate_score)

    # FACTOR 3: Explicit bonus for matched keywords (NEW)
    # Give increasing bonus for each matched keyword up to a cap
    hard_match_bonus = min(0.20, len(matched_hard_skills) * 0.04)  # 4% per match, max 20%
    soft_match_bonus = min(0.10, len(matched_soft_skills) * 0.02)  # 2% per match, max 10%
    matched_keyword_bonus = hard_match_bonus + soft_match_bonus

    print("Matched Keyword Bonus:", matched_keyword_bonus)

    # FACTOR 4: Bonus for extra skills
    hard_extra_bonus = min(0.10, len(extra_hard_skills) * 0.02)  # Cap at 10% bonus (reduced from 15%)
    print("Hard Extra Bonus:", hard_extra_bonus)

    soft_extra_bonus = min(0.05, len(extra_soft_skills) * 0.01)  # Cap at 5% bonus (reduced from 10%)
    print("Soft Extra Bonus:", soft_extra_bonus)

    extra_skills_bonus = hard_extra_bonus + soft_extra_bonus
    print("Extra Skill Bonus:", extra_skills_bonus)

    # FACTOR 5: Penalty for missing critical skills
    missing_critical_penalty = min(0.25, len(unmatched_hard_skills) * 0.05)
    print("Missing Critical Penalty:", missing_critical_penalty)

    # Final weighted score formula
    final_score = (base_score * 0.5) + (match_rate_score * 0.3) + (extra_skills_bonus * 0.1) - missing_critical_penalty

    # Ensure score is between 0 and 1, then convert to percentage
    final_score = max(0, min(1, final_score)) * 100

    print(final_score)

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


resume_path = BASE_DIR / 'media' / 'resumes' / 'FordDow_Izaak_Resume_2025.pdf'
resume = Resume(str(resume_path))

print(keyword_similarity_score(1, resume.resume_text))
