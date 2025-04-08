import os
import django
from django.conf import settings
from sentence_transformers import SentenceTransformer, util
from api.job_posting.job_posting import JobPosting
from comparator.resume.resume import Resume
import re

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')

django.setup()

model = SentenceTransformer('all-MiniLM-L6-v2')


def exhaustive_resume_fit(job_text: str, resume_text: str, threshold=0.6):
    """
    Compare job requirements with resume content using semantic similarity.

    Args:
        job_text: Text containing job requirements
        resume_text: Text extracted from resume
        threshold: Minimum similarity score to consider a match

    Returns:
        dict: Matching statistics and detailed results
    """
    # Preprocessing to extract cleaner segments
    job_lines = [line.strip() for line in job_text.splitlines() if line.strip() and len(line.strip()) > 10]

    # Process resume text into more meaningful chunks (sentences/paragraphs)
    resume_segments = []
    for paragraph in resume_text.split('\n\n'):
        # Split long paragraphs into sentences
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        for sentence in sentences:
            if sentence.strip() and len(sentence.strip()) > 10:
                resume_segments.append(sentence.strip())

    if not job_lines or not resume_segments:
        return {
            "score": 0.0,
            "matched": [],
            "unmatched_job_lines": job_lines,
            "match_count": 0,
            "total_requirements": len(job_lines)
        }

    # Encode all lines at once (batch processing)
    job_embeddings = model.encode(job_lines, convert_to_tensor=True)
    resume_embeddings = model.encode(resume_segments, convert_to_tensor=True)

    # Calculate full similarity matrix at once
    similarity_matrix = util.cos_sim(job_embeddings, resume_embeddings)

    matched = []
    matched_job_indices = set()

    # Adaptive threshold - for shorter resumes, be slightly more lenient
    adaptive_threshold = max(threshold - (0.05 if len(resume_segments) < 20 else 0), 0.5)

    # Find the best match for each job requirement
    for j in range(len(job_lines)):
        best_match_idx = None
        best_score = adaptive_threshold  # Use threshold as minimum acceptable score

        for r in range(len(resume_segments)):
            sim = similarity_matrix[j][r].item()
            if sim > best_score:
                best_score = sim
                best_match_idx = r

        if best_match_idx is not None:
            matched.append({
                "requirement": job_lines[j],
                "resume_match": resume_segments[best_match_idx],
                "score": round(best_score, 2)
            })
            matched_job_indices.add(j)

    # Get unmatched job requirements
    unmatched_job_lines = [job_lines[i] for i in range(len(job_lines)) if i not in matched_job_indices]

    # Calculate enhanced score
    if job_lines:
        # Coverage with higher weight (75%)
        coverage_score = (len(matched_job_indices) / len(job_lines)) * 100

        # Quality score with lower weight (25%)
        match_quality = sum(item["score"] for item in matched) / max(len(matched), 1)

        # Final weighted score calculation
        final_score = (coverage_score * 0.75) + (match_quality * 100 * 0.25)
    else:
        final_score = 0.0

    return {
        "score": round(final_score, 2),
        "matched": matched,
        "unmatched_job_lines": unmatched_job_lines,
        "match_count": len(matched_job_indices),
        "total_requirements": len(job_lines),
        "coverage_percent": round(len(matched_job_indices) / max(len(job_lines), 1) * 100, 1)
    }
resume_path = settings.BASE_DIR / 'media' / 'resumes' / 'Java-Developer-Resume-4.pdf'
resume = Resume(str(resume_path))

job_posting = JobPosting().create_from_json(1)

job_text = ""

if job_posting.job_requirements_must_have:
    job_text += "\n".join(str(item) for item in job_posting.job_requirements_must_have)
    job_text += "\n"  # Add separator between sections

if job_posting.job_requirements_nice_to_have:
    job_text += "\n".join(str(item) for item in job_posting.job_requirements_nice_to_have)

# Use a lower threshold for better matching
print(exhaustive_resume_fit(job_text, resume.resume_text, 0.6))