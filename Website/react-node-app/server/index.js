// server/index.js

const express = require("express");

const {spawn} = require('child_process');

//const childPython = spawn('python',['--version']);
const childPython = spawn('python',['server/Third_Website.py']);

const PORT = process.env.PORT || 3001;

const app = express();

let globedat = null;

childPython.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
  globedat = data.toString();
});

childPython.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});

app.get("/api", (req,res)=>{
  // Send a JSON response with the data from template.json
  if (globedat !== null) {
    const encodedHTML = JSON.stringify(globedat);
    res.json({ message: encodedHTML });
  } else {
    res.json({ message: "H" });
  }
})
  
  app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });

childPython.on('close',(code) => {
  console.log(`child process exited with code ${code}`);
});