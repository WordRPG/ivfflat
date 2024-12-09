import { PointLoader } from "../../src/frontend/utils/points_loader.js";
import { Point } from "../../src/frontend/utils/point.js";
import { BruteForceNNS } from "../../src/frontend/search/brute_force.js";

console.log("Loading points.")
let points = PointLoader.load("./data/sift/siftsmall/siftsmall_base.bin", 128) 
points = points.map((point, index) => new Point(index, point))

console.log("Building indexer.")
const indexer = new BruteForceNNS()
indexer.build(points)

console.log("Querying indexer.") 
const target = points[100] 
const k = 10 
console.log(indexer.nearest(target, k))