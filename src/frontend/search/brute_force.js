import * as operations from "ivfflat/src/frontend/utils/operations.js"
import * as measures from "ivfflat/src/frontend/utils/measures.js"

export class BruteForceNNS
{
    /** 
     * @param {Object} options 
     */
    constructor() {
        this.points = null
        this.measureFn = measures.euclideanDistance
    }

    // --- TREE CONSTRUCTION ---  // 
    build(points) {
        this.points = points 
    }

    // --- TREE QUERIES --- // 

    nearest(target, k) {
        const results = operations.nearestK(this.points, target, k, this.measureFn)
        const indices = results.map(x => x[0])
        const distances = results.map(x => x[1])
        return [indices, distances]
    }

    farthest(target, k) {
        const results = operations.farthestK(this.points, target, k, this.measureFn)
        const indices = results.map(x => x[0])
        const distances = results.map(x => x[1])
        return [indices, distances]
    }
}