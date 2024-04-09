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

// Define the /user-email route
app.get('/user-email', async (req, res) => {
  console.log("index")
  try {
      // Assuming you have user email in session after CAS authentication
      const userEmail = req.session.cas && req.session.cas.user && req.session.cas.user.attributes && req.session.cas.user.attributes.email;
      
      if (userEmail) {
          res.json({ email: userEmail });
      } else {
          res.status(404).send('User email not found in');
      }
  } catch (error) {
      console.error('Error retrieving user email:', error.message);
      res.status(500).send('Internal Server Error');
  }
});

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
    res.redirect('/admin');
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
