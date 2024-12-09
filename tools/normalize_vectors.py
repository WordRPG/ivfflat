from src.backend.utils.points_loader import PointLoader 
from src.backend.search.ivf_flat import IVFFlat
from src.backend.utils.point import Point
from src.backend.utils.points_loader import PointLoader
from src.backend.search.benchmarking import SearchBenchmarker
import os
import numpy as np
from sklearn.preprocessing import normalize

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

print("Loading vectors.")
points = PointLoader.load("./data/word-embeddings/glove-wiki-gigaword-50/vectors.bin", 50)

print("Normalizing vectors.")
points = np.array(points) 
points = normalize(points)

print("Saving vectors.")
points = points.tolist() 
PointLoader.save(
    "./data/word-embeddings/glove-wiki-gigaword-50/vectors.norm.bin", 
    points, 
    50
)