import { PointLoader } from "../../src/frontend/utils/points_loader.js";
import { Point } from "../../src/frontend/utils/point.js";
import { BruteForceNNS } from "../../src/frontend/search/brute_force.js";
import { Benchmarker } from "../../src/frontend/utils/benchmark.js";

const benchmarker = new Benchmarker()

console.log("Loading points.")
let points = PointLoader.load("./data/word-embeddings/glove-wiki-gigaword-50/vectors.norm.bin", 50) 
points = points.map((point, index) => new Point(index, point))

console.log("Building indexer.")
benchmarker.start("build")
const indexer = new BruteForceNNS()
indexer.build(points)
benchmarker.end("build")

console.log("Querying indexer.") 
const target = points[100] 
const k = 10 

benchmarker.start("query")
console.log(indexer.nearest(target, k))
benchmarker.end("query")


console.log(benchmarker.summary())