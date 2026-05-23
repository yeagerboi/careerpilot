import numpy as np

def calculate_fit_score(cv_vector: list[float], job_vector: list[float]) -> float:
    """Programmatic Cosine Similarity: (A · B) / (||A|| ||B||)"""
    a = np.array(cv_vector)
    b = np.array(job_vector)
    
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    similarity = dot_product / (norm_a * norm_b)
    return float(similarity * 100) # Return as percentage