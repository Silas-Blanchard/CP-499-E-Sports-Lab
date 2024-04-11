//index.js is the brains of the operation. It will call server with database.py and the HTML generator code (which is written in python). 

const express = require('express');
const http = require('http');
const { spawn } = require('node:child_process');
const app = express();
const server = http.createServer(app);
const { Server } = require("socket.io");
const { join } = require('path');
const session = require('express-session');
const { initializeCasAuth, checkWhitelist } = require('./content_gen/cas');

const childPython = spawn('python3', ['server/content_gen/six_website.py']);
const childPythonJSON = spawn('python3', ['server/content_gen/JSON-maker.py']);
const serverpython = spawn('python3', ['server/server with database.py']);
serverpython.on('exit', function (code) { 
  listening = null;
  console.log("PYTHON SERVER EXITED " + code);
 });

const PORT = process.env.PORT || 3001;
const io = new Server(server);

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

//this function sends JSON files, containing color data for the lab computers, to every isntance of the website.
async function notify() {
  while (true) {
    await sleep(5000)
    spawn('python3', ['server/content_gen/six_website.py']);
    const hey = spawn('python3', ['server/content_gen/JSON-maker.py']); //constantly updates computes with new colors
    hey.stdout.on('data', function (data) {
      var text = data.toString('utf8');
      var str = text.replace(/'/g, '\"');
      io.emit('update', str);
    });
  }
}

notify();

childPythonJSON.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

childPython.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});

app.use(session({
  secret: 'your_secret_key',
  resave: false,
  saveUninitialized: true,
}));


// Route to handle CAS authentication callback
app.get('/admin', (req, res, next) => {
  initializeCasAuth()(req, res, next);
}, (req, res) => {
  console.log('CAS authentication successful');

  // After CAS authentication, check whitelist
  checkWhitelist(req, res, () => {
    // User is on the whitelist, redirect to admin page
    console.log('User is on the whitelist.');
    console.log('Redirecting to admin page.');
    res.sendFile(join(__dirname, '/html_and_layout_data/admin_page.html'));
  }, () => {
    // User is not on the whitelist, redirect to main page
    console.log('User is not on the whitelist.');
    console.log('Redirecting to main page.');
    res.redirect('/');
  });
});

// Main page route
app.get('/', (req, res) => {
  res.sendFile(join(__dirname, '/html_and_layout_data/webber.html'));
});

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

childPython.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});
