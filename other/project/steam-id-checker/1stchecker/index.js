const fs = require('fs');
const { Worker } = require("worker_threads");

let ids = fs.readFileSync('input.txt', 'UTF-8').split(/\r?\n/);

console.log(`found ${ids.length}`)

let mode = true; // false = profile ids / true = group ids
let threads = 50;

for(let i = 0; i < threads; i++) {
    let data = {
        ids : ids.splice(0, ids.length / threads),
        mode: mode
    }
    new Worker("./check.js", { workerData: data });
}
