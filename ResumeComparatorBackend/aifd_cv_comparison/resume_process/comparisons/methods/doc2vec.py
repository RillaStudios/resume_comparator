import os
from gensim.models import Doc2Vec
from DjangoApp import settings
from numpy.linalg import norm
import numpy as np

def compare_job2vec(resume_text: str, job_posting_text: str) -> float:

    model_path = os.path.join(settings.BASE_DIR, 'ai_models', 'cv_job_maching.model')

    # Move this inside try block
    try:
        # Load the model
        model = Doc2Vec.load(model_path)

        v1 = model.infer_vector(resume_text.split())  # Vector for resume
        v2 = model.infer_vector(job_posting_text.split())  # Vector for job posting

        if norm(v1) == 0 or norm(v2) == 0:
            print("One of the vectors is zero, cannot compute similarity.")
            return 0

        similarity = 100 * (np.dot(v1, v2) / (norm(v1) * norm(v2)))

        return similarity

    except Exception as e:
        print(f"Error in ai_raw_compare: {e}")
        return 0