from src.backend.utils.points_loader import PointsLoader 
from src.backend.search.ivf_flat import IVFFlat
from src.backend.utils.point import Point
from src.backend.search.benchmarking import SearchBenchmarker
import os
import random
import json
import sys

random.seed(1234567890)

print("Loading points.")
points = PointsLoader.load("./data/word-embeddings/glove-wiki-gigaword-50/vectors.norm.bin", 50)
points = [Point(index, points[index]) for index in range(len(points))]

print("Building indexer.")
indexer = IVFFlat() 
indexer.points = points 
indexer.load("./data/indexers/glove-wiki-gigaword-50.10k.json")

print("Benchmarking indexer.")
benchmarker = SearchBenchmarker(points, indexer = indexer)

def query_fn(object_, target, k, probe_count = None):
    if probe_count:
        return object_.farthest(target, k, probe_count = probe_count)
    else:
        return object_.farthest(target, k)

benchmarker.query_fn = query_fn

BENCHMARK_COUNT = 1000
QUERY_COUNT     = 500
PROBE_COUNT     = int(sys.argv[1])
OUTPUT_FILE     = f"benchmark-{BENCHMARK_COUNT}-{QUERY_COUNT}-{PROBE_COUNT}.json"


targets = random.sample(points, BENCHMARK_COUNT)

recalls_all = [] 

i = 0
n = len(targets)
for target in targets: 
    print(f"Benchmarking {i} of {n}")
    recalls, times = benchmarker.run(target, QUERY_COUNT, PROBE_COUNT)
    recalls_all.append(recalls) 
    
    print("Recalls :", recalls)
    print("\tTime (BF)      :", times.duration("exact"))
    print("\tTime (Approx.) :", times.duration("approx"))

    i += 1

json.dump(recalls_all, open("./data/benchmarks/" + OUTPUT_FILE, "w"))