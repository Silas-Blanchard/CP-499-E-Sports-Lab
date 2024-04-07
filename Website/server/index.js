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

const PORT = process.env.PORT || 3001;
const io = new Server(server);

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

async function notify() {
  while (true) {
    await sleep(5000)
    spawn('python3', ['server/content_gen/six_website.py']);
    const hey = spawn('python3', ['server/content_gen/JSON-maker.py']);
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
    // If user is on the whitelist, redirect to admin page
    res.redirect('/admin');
  }, () => {
    // If user is not on the whitelist, redirect to main page
    res.redirect('/');
  });
});

// Main page route
app.get('/', (req, res) => {
  res.sendFile(join(__dirname, '/html_and_layout_data/webber.html'));
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on("updateComps", function (data) {
    console.log(data)
  });
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

server.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});

childPython.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});
