//the innumerable imports
const express = require('express');
const http = require('http');
const { spawn } = require('node:child_process');
const app = express();
const server = http.createServer(app);
const { Server } = require("socket.io")
const {join} = require('path')

const childPython = spawn('python3',['server/content_gen/six_website.py']);
const childPythonJSON = spawn('python3',['server/content_gen/JSON-maker.py']);
const childServer = spawn('python3',['server/content_gen/server with databaser.py']);

const fs = require('fs');

const PORT = process.env.PORT || 3001;

//var server  = app.listen(3001);
const io = new Server(server);

//sleep function that only works in async functions!
//
const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

//CAS!
//import caspackage from 'cas-authentication';

// const cas = new caspackage({
//   cas_url: 'https://cc-cas.com/cas', //replace with the proper cas website, please
//   service_url: 'http://esportscomm.coloradocollege.edu'
// });

//app.use(cas.bounce)

//We will forever update our clients forever (or until they inevitably disconnect)
async function notify(){
  while (true){
    await sleep(5000)
    spawn('python3',['server/content_gen/six_website.py']);
    const hey = spawn('python3',['server/content_gen/JSON-maker.py']);
    hey.stdout.on('data', function(data) {
      var text = data.toString('utf8');// buffer to string
      var str = text.replace(/'/g, '\"');//it does not like ' quotation marks it likes "
      io.emit('update', str);
  });
  }
}

notify()

//when our JSON maker goes off, we will have this print out the data. 
childPythonJSON.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

childPython.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});

app.get('/', (req, res) => {
  res.sendFile(join(__dirname, '/html_and_layout_data/webber.html'));
});

app.get('/admin', (req, res) => {
  var listening = spawn('python3',['server/content_gen/admin_page_datafill.py']);
  res.sendFile(join(__dirname, '/html_and_layout_data/admin_page.html'));
});

// app.get('/admin', cas.block, (req, res) => {
//   res.sendFile(join(__dirname, 'admin_page.html'));
// });

io.on('connection', (socket) => {
  socket.on("updateComps", function(data) {
  fs.writeFile('server/html_and_layout_data/unparsed.txt', data, (err) => {
      if (err) throw err;
  })
  var listening = spawn('python3',['server/content_gen/admin_update.py'])
  listening.on('exit', function (code) { 
    listening = null;
    console.log("EXITED " + code);
   });
  spawn('python3',['server/content_gen/six_website.py'])
  });

  socket.on("restore", function(data) {
    console.log("restore")
  });
});

server.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});

childPython.on('close',(code) => {
  console.log(`child process exited with code ${code}`);
});

