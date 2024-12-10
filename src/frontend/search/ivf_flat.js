import fs from "fs"
import { Point } from "../utils/point.js"
import { BruteForceNNS } from "./brute_force.js"
import { Heap } from "../utils/heap.js"
import { Benchmarker } from "../utils/benchmark.js"
import cluster from "cluster"
import * as measures from "ivfflat/src/frontend/utils/measures.js"

export class IVFFlat 
{
    constructor(source, measureFn = measures.euclideanDistance) {
        this.source = source 
        this.points = null 
        this.centroids = null 
        this.clusters = null
        this.measureFn = measureFn
        this.loadSource()
    }

    loadSource() {
        const data = this.source
        this.centroids = 
            data.centroids.map((value, index) => new Point(index, value))
        this.clusters = data.clusters
    }

    setPoints(points) {
        this.points = points
    }

    nearest(target, k, probeCount = 3) {
        const clusterCount = this.centroids.length 
        
        const benchmark = new Benchmarker()
        benchmark.start("sort-centroids")
        const closestCentroids = this.closestCentroids(target)
        benchmark.end("sort-centroids")

        const heap = new Heap({ 
            comparator: (a, b) => b[1] - a[1],
            maxSize : k
        })

        benchmark.start("closest-points")

        let probedCount = 0 
        while(probedCount < probeCount || heap.size() < k) {
            const probeClusterId = closestCentroids[0][probedCount] 
            const clusterPointIds = this.clusters[probeClusterId] 
            const clusterPoints = clusterPointIds.map((id) => this.points[id])
        
            if(clusterPoints.length == 0) {
                continue
            }

            for(let clusterPoint of clusterPoints) {
                const distance = this.measureFn(clusterPoint, target)
                heap.push([clusterPoint.id, distance])
            }

            probedCount += 1
        }

        benchmark.end("closest-points")

        const results = heap.extract()
        results.reverse() 

        const indices = results.map(x => x[0])
        const distances = results.map(x => x[1])

        return [indices, distances, benchmark]
    }

    closestCentroids(target) {
        const clusterCount = this.centroids.length 
        const indexer = new BruteForceNNS() 
        indexer.build(this.centroids) 
        return indexer.nearest(target, clusterCount)
    }

    farthest(target, k, probeCount = 3) {
        const clusterCount = this.centroids.length 
        
        const benchmark = new Benchmarker()
        benchmark.start("sort-centroids")
        const closestCentroids = this.farthestCentroids(target)
        benchmark.end("sort-centroids")

        const heap = new Heap({ 
            comparator: (a, b) => a[1] - b[1],
            maxSize : k
        })

        benchmark.start("farthest-points")

        let probedCount = 0 
        while(probedCount < probeCount || heap.size() < k) {
            const probeClusterId = closestCentroids[0][probedCount] 
            const clusterPointIds = this.clusters[probeClusterId] 
            const clusterPoints = clusterPointIds.map((id) => this.points[id])
        
            if(clusterPoints.length == 0) {
                continue
            }

            for(let clusterPoint of clusterPoints) {
                const distance = this.measureFn(clusterPoint, target)
                heap.push([clusterPoint.id, distance])
            }

            probedCount += 1
        }

        benchmark.end("farthest-points")

        const results = heap.extract()
        results.reverse() 

        const indices = results.map(x => x[0])
        const distances = results.map(x => x[1])

        return [indices, distances, benchmark]
    }

    farthestCentroids(target) {
        const clusterCount = this.centroids.length 
        const indexer = new BruteForceNNS() 
        indexer.build(this.centroids) 
        return indexer.farthest(target, clusterCount)
    }
}