import { IVFFlat } from "../../src/frontend/search/ivf_flat.js";
import { PointLoader } from "../../src/frontend/utils/points_loader.js";
import { Point } from "../../src/frontend/utils/point.js";
import { Benchmarker } from "../../src/frontend/utils/benchmark.js";

const benchmarker = new Benchmarker()

console.log("Loading points.")
let points = 
    PointLoader.load("./data/word-embeddings/glove-wiki-gigaword-50/vectors.norm.bin", 50) 
points = points.map((point, index) => new Point(index, point))

console.log("Building indexer.")
benchmarker.start("build")
const indexer = new IVFFlat("./data/indexers/glove-wiki-gigaword-50.10k.json")
indexer.setPoints(points)
benchmarker.end("build")

console.log("Querying indexer.") 
const target = points[30] 
const k = 10

benchmarker.start("query")
const results = indexer.nearest(target, k, 100)
benchmarker.end("query")

console.log(results[0])
console.log(results[1])
console.log(results[2].summary())
console.log(benchmarker.summary())