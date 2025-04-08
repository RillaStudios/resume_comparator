import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math

nlp = spacy.load("en_core_web_sm")  # medium model with vectors

def skill_similarity(skill1: str, skill2: str) -> float:
    vec1 = nlp(skill1).vector
    vec2 = nlp(skill2).vector
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return cosine_similarity([vec1], [vec2])[0][0]


def fuzzy_match_skills(job_skills, cv_skills, threshold=0.5):
    matched = []
    unmatched = []
    extras = []

    for job_skill in job_skills:
        best_sim = 0
        best_match = None
        for cv_skill in cv_skills:
            sim = skill_similarity(job_skill, cv_skill)
            if sim > best_sim:
                best_sim = sim
                best_match = cv_skill
        if best_sim >= threshold:
            matched.append((job_skill, best_match, best_sim))
        else:
            unmatched.append(job_skill)

    matched_cv_skills = {m[1] for m in matched}
    for cv_skill in cv_skills:
        if cv_skill not in matched_cv_skills:
            extras.append(cv_skill)

    return matched, unmatched, extras


def skill_matcher(jp_hard_skills, jp_soft_skills, cv_hard_skills, cv_soft_skills) -> dict:
    """
    Smart skill matcher using cosine similarity to account for semantic closeness.
    Returns a breakdown of matched/unmatched/bonus skills and a dynamic match score.

    @Author: IFD
    @Date: 2025-04-08
    """

    # Semantic matching
    matched_hard, unmatched_hard, extra_hard = fuzzy_match_skills(jp_hard_skills, cv_hard_skills)
    matched_soft, unmatched_soft, extra_soft = fuzzy_match_skills(jp_soft_skills, cv_soft_skills)

    # Base counts
    H = len(jp_hard_skills) or 1
    S = len(jp_soft_skills) or 1
    Eh = len(extra_hard)
    Es = len(extra_soft)
    Uh = len(unmatched_hard)
    Us = len(unmatched_soft)

    # --- Similarity-weighted core score ---
    hard_sim_sum = sum(sim for _, _, sim in matched_hard)
    soft_sim_sum = sum(sim for _, _, sim in matched_soft)

    # Use log scaling to handle long skill lists
    hard_coverage = math.log2(hard_sim_sum + 1) / math.log2(H + 1)
    soft_coverage = math.log2(soft_sim_sum + 1) / math.log2(S + 1)

    core_score = (hard_coverage * 0.6) + (soft_coverage * 0.2)

    # --- Bonus for extra skills (diminishing) ---
    hard_bonus = (1 - 1 / (1 + Eh)) * 0.1
    soft_bonus = (1 - 1 / (1 + Es)) * 0.05
    bonus = hard_bonus + soft_bonus

    # --- Final Score ---
    match_score = core_score + bonus
    match_score = max(0, min(1, round(match_score, 4)))  # Clamp between 0 and 1

    return {
        "matched_hard_skills": matched_hard,
        "unmatched_hard_skills": unmatched_hard,
        "matched_soft_skills": matched_soft,
        "unmatched_soft_skills": unmatched_soft,
        "bonus_hard_skills": extra_hard,
        "bonus_soft_skills": extra_soft,
        "match_score": match_score,
    }
