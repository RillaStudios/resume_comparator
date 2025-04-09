from api.job_posting.job_posting import JobPosting
from comparator.compare_utils.ai_tools.skill_extractor import extract_skills, get_raw_skills


def skill_matcher(resume_text: str, job_posting_id: int):
    """
    Matches job posting hard/soft skills with CV skills using semantic similarity.

    Returns a dictionary with matched/unmatched/extra skills.
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

    matched_hard = set(skills_jp_hard_list) & set(skills_cv_hard_list)
    unmatched_hard = set(skills_jp_hard_list) - set(skills_cv_hard_list)
    extra_hard = set(skills_cv_hard_list) - set(skills_jp_hard_list)

    matched_soft = set(skills_jp_soft_list) & set(skills_cv_soft_list)
    unmatched_soft = set(skills_jp_soft_list) - set(skills_cv_soft_list)
    extra_soft = set(skills_cv_soft_list) - set(skills_jp_soft_list)

    # Add at the end of skill_matcher function before the return statement
    score = __calculate_skill_score(
        matched_hard, unmatched_hard, extra_hard,
        matched_soft, unmatched_soft, extra_soft
    )

    return {
        "score": score,
        "matched_hard_skills": matched_hard,
        "unmatched_hard_skills": unmatched_hard,
        "extra_hard_skills": extra_hard,
        "matched_soft_skills": matched_soft,
        "unmatched_soft_skills": unmatched_soft,
        "extra_soft_skills": extra_soft
    }


def __calculate_skill_score(matched_hard, unmatched_hard, extra_hard,
                          matched_soft, unmatched_soft, extra_soft):
    """
    Calculate a weighted skill match score:
    - Hard skills are weighted more than soft skills
    - Extra skills provide small bonuses
    - Result is normalized to 0-100 scale
    """
    # Calculate weights
    total_hard_skills = len(matched_hard) + len(unmatched_hard)
    total_soft_skills = len(matched_soft) + len(unmatched_soft)

    # Avoid division by zero
    if total_hard_skills == 0 and total_soft_skills == 0:
        return 0

    # Base weights: hard skills count double
    hard_weight = 2
    soft_weight = 1

    # Calculate maximum possible score
    max_score = (total_hard_skills * hard_weight) + (total_soft_skills * soft_weight)

    # Calculate actual score
    actual_score = (len(matched_hard) * hard_weight) + (len(matched_soft) * soft_weight)

    # Add bonuses for extra skills
    bonus = 0
    bonus += len(extra_hard) * 0.5  # Extra hard skills bonus
    bonus += len(extra_soft) * 0.25  # Extra soft skills bonus

    # Calculate final score (0-100)
    if max_score > 0:
        raw_score = actual_score + bonus
        final_score = min((raw_score / max_score) * 100, 100)
    else:
        final_score = bonus * 10.0  # Only count bonuses if no required skills

    return final_score
