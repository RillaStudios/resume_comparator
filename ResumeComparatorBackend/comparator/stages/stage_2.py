from comparator.compare_utils.ai_tools.cosine_sim import skill_similarity
from comparator.compare_utils.text_tools.skill_matcher import skill_matcher

def keyword_similarity_score(resume_text: str, job_posting_id: int) -> dict:

    # Calculate the similarity score between the resume and job posting (Cosine Similarity)
    sim_score = skill_similarity(resume_text, job_posting_id)

    # Calculate the skill match score (Skill Matcher)
    matchings = skill_matcher(resume_text, job_posting_id)

    # Calculate the final score

    if sim_score > matchings['score']:
        final_score = ((matchings['score'] * 0.3) + (sim_score * 0.7))
    else:
        final_score = ((sim_score * 0.3) + (matchings['score'] * 0.7))

    # Create a dictionary to store the results
    results = {
        'final_score': final_score,
        'matched_skills': matchings['matched_hard_skills'],
        'missing_skills': matchings['unmatched_hard_skills']
    }

    return results
