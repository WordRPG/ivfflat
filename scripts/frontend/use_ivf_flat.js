import { IVFFlat } from "../../src/frontend/search/ivf_flat.js";
import { PointsLoader } from "../../src/frontend/utils/points_loader.js";
import { Point } from "../../src/frontend/utils/point.js";
import { Benchmarker } from "../../src/frontend/utils/benchmark.js";
import fs from "fs"

const benchmarker = new Benchmarker()

console.log("Loading points.")
let points = 
    PointsLoader.load("./data/word-embeddings/wordrpg-glove-2024/vectors.norm.bin", 50) 
points = points.map((point, index) => new Point(index, point))

console.log("Building indexer.")
benchmarker.start("build")
const source = 
    JSON.parse(
        fs.readFileSync(
            "./data/indexers/wordrpg-glove-2024/indexer.json"
        )
    )
const indexer = 
    new IVFFlat(source) 
indexer.setPoints(points)
benchmarker.end("build")

console.log("Querying indexer.") 
const target = points[20] 
const k = 10

benchmarker.start("query")
const results = indexer.nearest(target, k, 150)
benchmarker.end("query")

console.log(results[0])
console.log(results[1])
console.log(results[2].summary())
console.log(benchmarker.summary())