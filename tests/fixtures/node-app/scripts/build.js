const fs = require("fs");
fs.mkdirSync("dist", { recursive: true });
fs.writeFileSync("dist/index.html", "<!doctype html><title>fixture</title><h1>ok</h1>\n");
console.log("build ok");
