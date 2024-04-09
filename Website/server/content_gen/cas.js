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
  const userEmail = req.session.cas && req.session.cas.user;
  const adminWhitelist = ['jlauer2023@coloradocollege.edu', 'q_sebso@gcoloradocollege.edu'];
  if (userEmail && adminWhitelist.includes(userEmail.toLowerCase())) {
    console.log(adminWhitelist.includes(userEmail.toLowerCase()));
    console.log(userEmail && adminWhitelist.includes(userEmail.toLowerCase()));
    console.log(req.session.cas);
    console.log(req.session.cas.user);
    console.log(req.session.cas.userEmail);
    // If user is on the whitelist, proceed to the next middleware
    res.redirect('/admin');
    console.log('IT WORKED, WHY ARE YOU NOT GOING?');
  } else {
    // If user is not on the whitelist, redirect to the main page
    res.redirect('/');
    console.log('User is not on the list');
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

