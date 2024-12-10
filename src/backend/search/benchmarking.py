from .brute_force import BruteForceNNS
from src.backend.utils.benchmark import Benchmarker

class SearchBenchmarker: 
    def __init__(self, points, indexer):
        self.points     = points 
        self.indexer    = indexer 

        # --- build exact
        self.exact      = BruteForceNNS() 
        self.exact.build(points)


    def query_fn(self, object_, target, k, probe_count = None):
        if probe_count:
            return object_.nearest(target, k, probe_count = probe_count)
        else:
            return object_.nearest(target, k,)

    
    def run(self, target, k = 10, probe_count = 3): 
        benchmark = Benchmarker()

        # --- query exact 
        benchmark.start("exact") 
        expected = self.query_fn(self.exact, target, len(self.points))
        benchmark.end("exact")

        # --- query indexer 
        benchmark.start("approx")
        observed = self.query_fn(self.indexer, target, k, probe_count = probe_count)
        benchmark.end("approx")

        recalls  = [-1 for i in range(11)]
        
        # --- recall keypoints 
        prev_recall = 0 
        s = k
        while prev_recall <= 0.99: 
            s += 1 
            recall = self.recall(expected[0][:s], observed[0])
            if recall == 0.99:
                recall = 1.0
            rounded_recall = int(recall * 10)
            if recalls[rounded_recall]  == -1:
                recalls[rounded_recall] = s
            prev_recall = recall
            if s > 10000: 
                print(s, recall, end="\r")

        return recalls, benchmark
    
    def recall(self, expected, observed): 
        expectedIds = set(expected.tolist())
        observedIds = observed

        correct = 0
        for observedId in observedIds: 
            if observedId in expectedIds:
                correct += 1 
            
        return correct / len(observedIds)