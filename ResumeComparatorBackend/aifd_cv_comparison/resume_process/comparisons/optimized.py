from gensim.models import Doc2Vec
from aifd_cv_comparison.models.model_loader import get_model
from numpy.linalg import norm
import numpy as np
from aifd_cv_comparison.utils.resume import Resume
from api.models import JobPosting

# Load models once at module level
_d2v_model = None
_nlp_model = None

def _get_d2v_model():
    global _d2v_model
    if _d2v_model is None:
        try:
            d2v_path = get_model('doc2vec').model
            _d2v_model = Doc2Vec.load(d2v_path)
        except Exception as e:
            print(f"Error loading Doc2Vec model: {e}")
    return _d2v_model

def _get_nlp_model():
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = get_model('spacy_lg').model
        except Exception as e:
            print(f"Error loading spaCy model: {e}")
    return _nlp_model

def optimized_resume_comparison(resume: Resume, job_posting: JobPosting) -> float:
    # Get cached models
    model = _get_d2v_model()
    nlp = _get_nlp_model()

    if not model or not nlp:
        print("Models could not be loaded")
        return 0

    # Move this inside try block
    try:

        """
        GET THE RESUME SKILLS AND JOB POSTING REQUIRED SKILLS SIMILARITY
        """
        resume_skills = nlp(resume.skills if resume.skills else "")
        job_req_skills = nlp(job_posting.skills_qual_required if job_posting.skills_qual_required else "")

        #Score for resume skills - job posting required skills
        req_skill_score = resume_skills.similarity(job_req_skills)

        print("Required skill score:", req_skill_score)

        """
        GET THE RESUME AND JOB POSTING NICE TO HAVE SKILLS SIMILARITY
        """
        job_nice_skills = nlp(job_posting.skills_qual_nice_to_have if job_posting.skills_qual_nice_to_have else "")

        #Score for resume skills - job posting nice to have skills
        nice_skill_score = resume_skills.similarity(job_nice_skills)

        print("Nice skill score:", nice_skill_score)

        """
        GET THE RESUME EXPERIENCE AND JOB POSTING EXPERIENCE SIMILARITY
        """
        resume_experience = nlp(resume.experience if resume.experience else "")
        job_experience = nlp(job_posting.experience_required if job_posting.education_required else "")

        # Calculate similarity between resume experience and job responsibilities
        experience_score = resume_experience.similarity(job_experience)

        print("Experience score:", experience_score)

        """
        GET THE RESUME EDUCATION AND JOB POSTING EDUCATION REQUIREMENTS SIMILARITY
        """
        resume_education = nlp(resume.education if resume.education else "")
        job_req_education = nlp(job_posting.education_required if job_posting.education_required else "")

        # Calculate similarity between resume education and job education requirements
        education_score = resume_education.similarity(job_req_education)

        print("Education score:", education_score)

        """
        GET THE RESUME AND JOB POSTING SUMMARY SIMILARITY
        """
        resume_summary = nlp(resume.summary if resume.summary else "")
        job_summary = nlp(job_posting.summary if job_posting.summary else "")

        # Calculate similarity between resume summary and job summary
        summary_score = resume_summary.similarity(job_summary)

        print("Summary score:", summary_score)

        """
        FINALLY DO A DOC2VEC COMPARISON BETWEEN THE RESUME AND JOB POSTING
        """
        r5 = model.infer_vector(resume.raw_text.split() if resume.raw_text else [""])
        j5 = model.infer_vector(job_posting.get_text().split())

        # Calculate similarity between resume and job posting
        doc_score = get_score(r5, j5)

        # Calculate weighted final score (0-100 scale)
        # Note:
        # If doc score is greater than 50, we give more weight to the doc2vec score
        # if doc score is less, we give equal weight to all scores. This is to try
        # to avoid the doc2vec score being too dominant when it is low.
        if doc_score > 50:
            base_score = (
                0.2 * req_skill_score * 100 +  # Required skills (20%)
                0.1 * experience_score * 100 +  # Experience (20%)
                0.1 * education_score * 100 +  # Education (20%)
                0.05 * nice_skill_score * 100 +  # Nice-to-have skills (20%)
                0.05 * summary_score * 100 +  # Summary alignment (20%)
                0.5 * doc_score * 100  # Doc2Vec score (50%)
            )

        else:
            # Get all scores in a list
            all_scores = [req_skill_score, experience_score, education_score, nice_skill_score, summary_score]

            # Sort scores in descending order
            sorted_scores = sorted(all_scores, reverse=True)

            print(doc_score)

            # Calculate weighted score: 30% for each top score, 5% for each bottom score
            base_score = (
                    0.25 * sorted_scores[0] * 100 +  # Top score (30%)
                    0.25 * sorted_scores[1] * 100 +  # Second score (30%)
                    0.25 * sorted_scores[2] * 100 +  # Third score (30%)
                    0.125 * sorted_scores[3] * 100 +  # Fourth score (5%)
                    0.125 * sorted_scores[4] * 100  # Fifth score (5%)
            )

        # Cap at 100 if needed
        final_score = min(100, base_score)

        return final_score

    except Exception as e:
        print(f"Error in optimized comparison: {e}")
        return 0

def get_score(v1: np.ndarray, v2: np.ndarray) -> float:
    if norm(v1) == 0 or norm(v2) == 0:
        print("One of the vectors is zero, cannot compute similarity.")
        return 0

    return 100 * (np.dot(v1, v2) / (norm(v1) * norm(v2)))