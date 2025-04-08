from sentence_transformers import SentenceTransformer, util

# Load the model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def match_skills(jp_skills, cv_skills, threshold=0.75):
    """
    Matches a list of job posting skills to a list of CV skills based on similarity.

    Returns:
        matched: list of (jp_skill, cv_skill, score)
        unmatched: list of jp_skills that had no good match
        extras: list of cv_skills that were not matched to any jp_skill
    """
    if not jp_skills or not cv_skills:
        return [], jp_skills, cv_skills

    jp_embeddings = model.encode(jp_skills, convert_to_tensor=True)
    cv_embeddings = model.encode(cv_skills, convert_to_tensor=True)

    matched = []
    unmatched = []
    matched_cv_indices = set()

    for idx, jp_skill in enumerate(jp_skills):
        similarity_scores = util.cos_sim(jp_embeddings[idx], cv_embeddings)[0]
        best_match_idx = similarity_scores.argmax().item()
        best_score = similarity_scores[best_match_idx].item()

        if best_score >= threshold:
            matched.append((jp_skill, cv_skills[best_match_idx], round(best_score, 2)))
            matched_cv_indices.add(best_match_idx)
        else:
            unmatched.append(jp_skill)

    extras = [cv for i, cv in enumerate(cv_skills) if i not in matched_cv_indices]
    return matched, unmatched, extras


def skill_matcher(jp_hard_skills, jp_soft_skills, cv_hard_skills, cv_soft_skills, threshold=0.75):
    """
    Matches job posting hard/soft skills with CV skills using semantic similarity.

    Returns a dictionary with matched/unmatched/extra skills.
    """
    matched_hard, unmatched_hard, extra_hard = match_skills(jp_hard_skills, cv_hard_skills, threshold)
    matched_soft, unmatched_soft, extra_soft = match_skills(jp_soft_skills, cv_soft_skills, threshold)

    return {
        "matched_hard_skills": matched_hard,
        "unmatched_hard_skills": unmatched_hard,
        "extra_hard_skills": extra_hard,
        "matched_soft_skills": matched_soft,
        "unmatched_soft_skills": unmatched_soft,
        "extra_soft_skills": extra_soft
    }
