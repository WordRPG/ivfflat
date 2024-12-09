import numpy as np 

class BruteForceNNS: 
    def __init__(self): 
        self.points = None

    def build(self, points): 
        self.points = np.array([x.value for x in points])

    def nearest(self, target, k): 
        query_points = self.points
        target = np.array(target.value)
    
        dist = np.linalg.norm(query_points - target, axis=1)
        sorted_indices = np.argsort(dist)
        indices = sorted_indices[:k]
        distances = dist[sorted_indices[:k]]
        
        return indices, distances

    def farthest(self, target, k):
        query_points = self.points
        target = np.array(target.value)

        dist = np.linalg.norm(query_points - target, axis=1)
        sorted_indices = np.argsort(dist)[::-1]
        indices = sorted_indices[:k]
        distances = dist[sorted_indices[:k]]
    
        return indices, distances
 

   