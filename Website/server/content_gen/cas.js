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
  try {
    // Check if user email is available in session attributes
    const userEmail = req.session.cas && 
                      req.session.user &&
                       req.session.cas.user && 
                       req.session.cas.user.attributes && 
                       req.session.cas.user.attributes.email;
    
    // Whitelisted email addresses
    const adminWhitelist = ['jlauer2023@ColoradoCollege.edu', 'q_sebso@gColoradoCollege.edu'];

    // Log the current user email and whitelist status
    // console.log('User email:', userEmail);
    // console.log('Admin whitelist:', adminWhitelist);

    // console.log('Session data:', req.session);
    // If you expect the user details to be under `req.session.user`, log this:
    // console.log('User details:', req.session.user);
    console.log('User details and email:', req.session.user.email);
    
    // Check if the user email is in the whitelist
    const isWhitelisted = req.session.user.email && adminWhitelist.includes(req.session.user.email);
    
    // If user is on the whitelist, proceed to the next middleware
    if (isWhitelisted) {
      console.log('User is on the whitelist.');
      console.log('Redirecting to admin page.');
      res.redirect('/admin');
    } else {
      // If user is not on the whitelist, redirect to the main page
      console.log('User is not on the whitelist.');
      console.log('Redirecting to main page.');
      res.redirect('/');
    }
  } catch (error) {
    // Log any errors that occur during whitelist checking
    console.error('Error checking whitelist:', error.message);
    res.redirect('/'); // Redirect to main page in case of error
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

