//the innumerable imports
const express = require('express');
const http = require('http');
const { spawn } = require('node:child_process');
const app = express();
const server = http.createServer(app);
const { Server } = require("socket.io")
const {join} = require('path')

const childPython = spawn('python3',['server/six_website.py']);
const childPythonJSON = spawn('python3',['server/JSON-maker.py']);

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

async function notify(){
  while (true){
    await sleep(10000)
    spawn('python3',['server/six_website.py']);
    const hey = spawn('python3',['server/JSON-maker.py']);
    hey.stdout.on('data', function(data) {
      var text = data.toString('utf8');// buffer to string
      var str = text.replace(/'/g, '\"');
      io.emit('update', str);
  });
  }
}

//one line of code and we will forever update our clients forever (or until they inevitably disconnect)
notify()

//when our JSON maker goes off, we will have this print out the data. 
//HTML doesn't do that since we just serve the file once initially.
childPythonJSON.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

childPython.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});

app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'webber.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(join(__dirname, 'admin_page.html'));
});

// app.get('/admin', cas.block, (req, res) => {
//   res.sendFile(join(__dirname, 'admin_page.html'));
// });

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

  
server.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});

childPython.on('close',(code) => {
  console.log(`child process exited with code ${code}`);
});
