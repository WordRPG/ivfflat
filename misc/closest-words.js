import { IVFFlat } from "ivfflat/src/frontend/search/ivf_flat.js"
import { Random } from "../src/frontend/utils/random.js"
import { PointLoader } from "../src/frontend/utils/points_loader.js"
import { Point } from "../src/frontend/utils/point.js"
import fs from "fs"
import readlinkSync from 'readline-sync';

const random = new Random(Math.random() * 10000)

// --- specify embedding folder --- // 
const embeddingFolder = "./data/word-embeddings/glove-wiki-gigaword-50"

// --- load vocabulary and embeddings --- // 
console.log("Loading vocabulary.")
let vocabulary = 
    fs.readFileSync(embeddingFolder + "/vocabulary.txt").toString().split("\n")

// --- create word index --- //
let wordIndex = {}
for(let i = 0; i < vocabulary.length; i++) {
    wordIndex[vocabulary[i]] = i
}

// --- load vectors --- //
console.log("Loading points.")
let vectors = 
    PointLoader.load(embeddingFolder + "/vectors.norm.bin", 50) 
vectors = vectors.map((vector, index) => new Point(index, vector))

console.log("Building indexer.")
const indexer = new IVFFlat("./data/indexers/glove-raw/glove-wiki-gigaword-50.5k.json")
indexer.setPoints(vectors)

let correct = 0 
let wrong = 0

while(true) {
// --- picnic --- // 
    let wordId = random.randInt(0, vocabulary.length - 1)
    let vector = vectors[wordId]
    let word = vocabulary[wordId]

    // --- get top 500 words --- // 
    const top500 = indexer.nearest(vector, 500, 100)
    const last500 = indexer.farthest(vector, 500, 100)


    // --- get random word --- //
    const wordA = random.choice(top500[0]) 
    const wordB = random.choice(last500[0])

    let shuffled = random.shuffle([wordA, wordB])

    console.log("Key Word: " + word) 
    console.log("========================")
    console.log("[1] " + vocabulary[shuffled[0]]) 
    console.log("[2] " + vocabulary[shuffled[1]]) 

    
    const answer = readlinkSync.question("Which is closest? ")
    console.log("Correct : " + vocabulary[wordA])
    if(vocabulary[shuffled[parseInt(answer - 1)]] == vocabulary[wordA]) {
        console.log("You are correct")
        correct += 1
    } else {
        console.log("You are wrong.")
        wrong += 1
    }

    console.log(`[CORRECT: ${correct}] [WRONG: ${wrong}]`)




    console.log("----------------------------------------")
}