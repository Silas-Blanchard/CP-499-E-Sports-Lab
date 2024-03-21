const express = require('express');
const session = require('express-session');
const CASAuthentication = require('cas-authentication');

const app = express();

// Set up CAS authentication
const cas = new CASAuthentication({
  cas_url: 'https://cas.coloradocollege.edu/cas',
  service_url: 'http://esportscomm.coloradocollege.edu/login/cas',
  session_info: 'user',
});

// Initialize express-session middleware
app.use(session({
  secret: 'your_secret_key',
  resave: false,
  saveUninitialized: true,
}));

// Middleware to initialize CAS authentication
app.use(cas.bounce);

// Routes
app.get('/', (req, res) => {
  res.render('index');
});

// Route to handle CAS authentication callback
app.get('/login/cas', cas.authenticate, (req, res) => {
  res.redirect('/admin');
});

app.get('/admin', (req, res) => {
  if (req.session.user) {
    res.render('admin');
  } else {
    res.redirect('/');
  }
});

// Logout route
app.get('/logout', cas.logout);

// Set up EJS as the view engine
app.set('view engine', 'ejs');

// Set up static files directory
app.use(express.static('public'));

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});
