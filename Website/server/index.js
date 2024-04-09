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

// Route to handle CAS authentication callback and whitelist check
app.get('/admin', (req, res, next) => {
  // Initialize CAS authentication middleware
  initializeCasAuth()(req, res, () => {
    // After CAS authentication, check whitelist
    const userEmail = req.session.cas && req.session.cas.user.attributes.email;
    const adminWhitelist = ['jlauer2023@coloradocollege.edu', 'q_sebso@gcoloradocollege.edu'];
    if (userEmail && adminWhitelist.includes(userEmail.toLowerCase())) {
      // If user is on the whitelist, redirect to admin page
      console.log('CAS authentication successful');
      console.log('User is on the whitelist');
      res.redirect('/admin');
    } else {
      // If user is not on the whitelist, redirect to main page
      console.log('CAS authentication successful');
      console.log('User is not on the whitelist');
      res.redirect('/');
    }
  });
});


// Main page route
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

childPython.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});

