from src.backend.utils.points_loader import PointLoader 
from src.backend.search.ivfflat import IVFFlat
from src.backend.utils.point import Point

print("Loading points.")
points = PointLoader.load("./data/sift/siftsmall/siftsmall_base.bin", 128)
points = [Point(index, points[index]) for index in range(len(points))]

print("Building indexer.")
indexer = IVFFlat() 
indexer.build(points)

print("Querying indexer.")
target = points[100] 
k      = 10 
print(indexer.nearest(target, 10))
