""" 
    Simple IVF-Flat Implementation using Scikit-Learn K-Means
""" 
from sklearn.cluster import KMeans
from .brute_force import BruteForceNNS
import numpy as np
from src.backend.utils.point import Point
from src.backend.utils.benchmark import Benchmarker
from src.backend.utils.heap import Heap
import src.backend.utils.measures as measures

class IVFFlat: 
    def __init__(
        self, 
        cluster_count = 1000, 
        random_state  = 1234567890,
        max_iter      = 10,
        verbose       = 10,
        init          = "random",
        n_init        = 1,
        measure_fn    = measures.euclidean_distance
    ):
        self.cluster_count = cluster_count
        self.random_state  = random_state 
        self.points        = None 
        self.clusterer     = None
        self.verbose       = verbose 
        self.init          = init
        self.n_init        = n_init
        self.max_iter      = max_iter
        self.measure_fn    = measure_fn
        
    def build(self, points): 
        self.points = points
        self.clusterer = KMeans(
            n_clusters = self.cluster_count,
            random_state = self.random_state, 
            init = self.init,
            n_init = self.n_init,
            verbose = self.verbose,
            max_iter = self.max_iter
        )
        query_points = np.array([point.value for point in self.points])
        self.clusterer.fit(query_points)

        # --- get centroids 
        self.centroids = \
            [   
                Point(index, self.clusterer.cluster_centers_[index]) 
                for index in range(len(self.clusterer.cluster_centers_))
            ]

        # --- get cluster assignments
        self.clusters = [[] for i in range(len(self.centroids))]
        for i in range(len(self.clusterer.labels_)): 
            self.clusters[self.clusterer.labels_[i]].append(i)

    def nearest(self, target, k=10, probe_count=3): 
        cluster_count = self.cluster_count 

        benchmark = Benchmarker() 
        benchmark.start("sort-centroids")
        closest_centroids = self.closest_centroids(target) 
        benchmark.end("sort-centroids")

        heap = Heap(comparator=lambda a, b: b[1] - a[1], max_size=k)

        benchmark.start("closest-points")
        
        probed_count  = 0 
        while probed_count < probe_count or heap.size() < k: 
            probe_cluster_id = closest_centroids[0][probed_count]
            cluster_point_ids = self.clusters[probe_cluster_id]
            cluster_points = [self.points[id_] for id_ in cluster_point_ids]
            
            if len(cluster_points) == 0: 
                continue

            for cluster_point in cluster_points:
                distance = self.measure_fn(cluster_point, target)
                heap.push([cluster_point.id, distance])

            probed_count += 1

        benchmark.end("closest-points")

        if self.verbose: 
            print(benchmark.summary())

        results = heap.extract() 
        results.reverse()

        indices = [x[0] for x in results]
        distances = [x[1] for x in results]

        return indices, distances, benchmark

    def closest_centroids(self, target, k = 10, probe_count = 3): 
        cluster_count = self.cluster_count
        indexer = BruteForceNNS() 
        indexer.build(self.centroids)
        return indexer.nearest(target, cluster_count)

    def farthest(self, target, k=10, probe_count=3): 
        cluster_count = self.cluster_count 

        benchmark = Benchmarker() 
        benchmark.start("sort-centroids")
        closest_centroids = self.closest_centroids(target) 
        benchmark.end("sort-centroids")

        heap = Heap(comparator=lambda a, b: a[1] - b[1], max_size=k)

        benchmark.start("closest-points")
        
        probed_count  = 0 
        while probed_count < probe_count or heap.size() < k: 
            probe_cluster_id = closest_centroids[0][probed_count]
            cluster_point_ids = self.clusters[probe_cluster_id]
            cluster_points = [self.points[id_] for id_ in cluster_point_ids]
            
            if len(cluster_points) == 0: 
                continue

            for cluster_point in cluster_points:
                distance = self.measure_fn(cluster_point, target)
                heap.push([cluster_point.id, distance])

            probed_count += 1

        benchmark.end("closest-points")

        if self.verbose: 
            print(benchmark.summary())

        indices = [x[0] for x in results]
        distances = [x[1] for x in results]

        return indices, distances, benchmark

    def farthest_centroids(self, target, k=10, probe_count=3):
        cluster_count = self.cluster_count
        indexer = BruteForceNNS() 
        indexer.build(self.centroids)
        return indexer.farthest(target, cluster_count)
