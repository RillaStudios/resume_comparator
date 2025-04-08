from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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