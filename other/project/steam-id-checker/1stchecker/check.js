import fetch from "node-fetch";
const { workerData } = require("worker_threads");
const fs = require("fs");

let apikey = "4E0ED6FC04965377A9FA48DC40CFE57D";

let mode = workerData.mode;
let ids = workerData.ids;

let url = mode ? "https://steamcommunity.com/actions/AvailabilityCheck?&type=groupLink&value=" : `http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=${apikey}&vanityurl=`;

function check(id) {
  fetch(url + id)
    .then((res) => res.text())
    .then((body) => {
      if (body.includes("already in use by another group") || body.includes("steamid")) {
        console.log(`${id} is taken`);
      } else {
        console.log(`${id} is free`);
        fs.appendFileSync("output.txt", `${id}\n`);
      }
    })
    .catch(() => {
      setTimeout(() => {
        check(id);
      }, 1000);
    })
    .then(() => {
      if (ids.length > 0) {
        check(ids.splice(0, 1));
      }
    });
}

check(ids.splice(0, 1));
