// server/index.js

import express from 'express';
import { createServer } from 'node:http';

import {spawn} from 'child_process';

import { Server } from "socket.io";
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

//const childPython = spawn('python',['--version']);
const childPython = spawn('python',['server/Third_Website.py']);

const PORT = process.env.PORT || 3001;

const app = express();

var server  = app.listen(3000);
const io = new Server(server);

let globedat = null;

childPython.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
  globedat = data.toString();
});

childPython.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});

app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'webber.html'));
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

  
  app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });

childPython.on('close',(code) => {
  console.log(`child process exited with code ${code}`);
});