from src.backend.utils.points_loader import PointsLoader 
from src.backend.search.ivf_flat import IVFFlat
from src.backend.utils.point import Point
import os

print("Loading points.")
points = \
    PointsLoader.load("./data/word-embeddings/wordrpg-glove-2024/vectors.norm.bin", 50)
points = \
    [Point(index, points[index]) for index in range(len(points))]

print("Building indexer.")
indexer = IVFFlat(
    max_iter = 10,
    cluster_count = 5000
) 
if os.path.exists("./temp/indexer.json"):
    indexer.points = points 
    indexer.load("./temp/indexer.json")
else:
    indexer.build(points)


print("Querying indexer.")
target = points[100] 
k      = 20
results = indexer.nearest(target, 10, 3)
print(results[0])
print(results[1])
print(results[2].summary())


print("Saving indexer.") 
indexer.save("./temp/indexer.json")