const session = require('express-session');
const CASAuthentication = require('cas-authentication');

// Set up CAS authentication
const cas = new CASAuthentication({
  cas_url: 'https://cas.coloradocollege.edu/cas',
  service_url: 'http://esportscomm.coloradocollege.edu',
  session_info: 'user',
});

// Middleware to initialize CAS authentication
function initializeCasAuth() {
  return cas.bounce;
}


// Middleware to check whitelist
function checkWhitelist(req, res, next) {
    // Whitelisted email addresses
    const adminWhitelist = ['jlauer2023@ColoradoCollege.edu', 'q_sebso@ColoradoCollege.edu', 's_blanchard@ColoradoCollege.edu'];

    console.log('User details and email:', req.session.user.email);
    
    // Check if the user email is in the whitelist
    const isWhitelisted = req.session.user.email && adminWhitelist.includes(req.session.user.email);
    
    // If user is on the whitelist, proceed to the next middleware
    if (isWhitelisted) {
      console.log('User is on the whitelist.');
      console.log('Redirecting to admin page.');
      next();
    } else {
      // If user is not on the whitelist, redirect to the main page
      console.log('User is not on the whitelist.');
      console.log('Redirecting to main page.');
      res.redirect('/');
    }
}



// Logout route
function logout(req, res) {
  cas.logout(req, res);
}

module.exports = {
  initializeCasAuth,
  checkWhitelist,
  logout
};

