import numpy as np
from scipy.spatial.distance import cosine

# Squared Euclidean Distance
def squared_euclidean_distance(A, B):
    # Convert A and B to numpy arrays if they are not already
    A, B = np.array(A.value), np.array(B.value)
    return np.sum((A - B) ** 2)

# Euclidean Distance
def euclidean_distance(A, B):
    return np.sqrt(squared_euclidean_distance(A, B))

# Cosine Distance
def cosine_distance(A, B):
    # Use scipy's cosine function which returns cosine distance
    return 1 - cosine(A.value, B.value)

# Manhattan Distance
def manhattan_distance(A, B):
    # Convert A and B to numpy arrays if they are not already
    A, B = np.array(A.value), np.array(B.value)
    return np.sum(np.abs(A - B))
