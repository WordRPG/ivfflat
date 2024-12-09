/**
 * Point Loader Utility
 */
import * as helpers from "ivfflat/src/frontend/utils/helpers.js"
import fs from "fs"

export class PointsLoader 
{
    /**
     * Loads a BA2D file into an array.
     */
	static load(filePath, dims, { batchSize = 200000, onLoadPoints = null } = {}) {
		const contents = fs.readFileSync(filePath)
		let subArrays = []
		const subArraySize = dims * 4
		const batchSizeBytes = subArraySize * batchSize
		const vectorCount = contents.length / subArraySize
		batchSize = Math.min(batchSize, vectorCount)
		let count = 0
		for(let i = 0; i < contents.length; i += batchSizeBytes) {
			const subArrayBytes = contents.slice(i, i + batchSizeBytes) 
			const subArrayAll = helpers.decodeBytesToFloatArray(subArrayBytes)
			const subArrayChunks = helpers.subdivide(subArrayAll, batchSize)
			subArrays = subArrays.concat(subArrayChunks)
			if(onLoadPoints) onLoadPoints(subArrayChunks, count)
			count +=1
		}
		return subArrays
    }   

    /** 
     * Saves a 2D array into a BA2D file.
     */
    static save(filePath, array, dims, { batchSize = 250000, onSavePoints = null } = {}) {
		let buffer = []
		batchSize = Math.min(batchSize, array.length)
		if(fs.existsSync(filePath)) {
			fs.unlinkSync(filePath)
		}
		let count = 0
		for(let i = 0; i < array.length; i++) {
			const subArray = array[i]
			if(i > 0 && i % batchSize == 0) {
				const bufferFlat = helpers.flatten(buffer)
				const bytes = helpers.encodeFloatArrayToBytes(bufferFlat)
				fs.appendFileSync(filePath, bytes)
				buffer = []
				if(onSavePoints) onSavePoints(buffer, count)
			}
			buffer.push(subArray)
			count += 1
		}
		
		const bufferFlat = helpers.flatten(buffer)
		const bytes = helpers.encodeFloatArrayToBytes(bufferFlat)
		if(onSavePoints) onSavePoints(buffer, count)
						
		fs.appendFileSync(filePath, bytes)
    }
}