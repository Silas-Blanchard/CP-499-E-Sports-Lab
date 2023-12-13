// server/index.js

import express from 'express';
import { createServer } from 'node:http';

import {spawn} from 'child_process';

import { Server } from "socket.io";

import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Spawn the Python child process
const childPython = spawn('python', ['server/Third_Website.py']);

const PORT = process.env.PORT || 3002;

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "*", // Be sure to restrict this in production
    methods: ["GET", "POST"]
  }
});

let globedat = null;

childPython.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
  globedat = data.toString();
  io.emit('update', globedat); // Emit the data to all connected clients
});

childPython.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'webber.html'));
});

io.on('connection', (socket) => {
  console.log('a user connected');

  // Optionally emit the latest data as soon as the client connects
  if (globedat) {
    socket.emit('update', globedat);
  }

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

// Use httpServer.listen instead of app.listen to include Socket.IO
httpServer.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});

childPython.on('close', (code) => {
  console.error(`child process exited with code ${code}`);
});

app.get('/webber', (req, res) => {
  res.sendFile(join(__dirname, 'webber.html'));
});

