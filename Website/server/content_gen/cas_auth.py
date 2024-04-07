from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session
from cas import CASClient

app = Flask(__name__)
app.secret_key = 'espots_lab_one'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

cas_url = 'https://cas.coloradocollege.edu/cas'
app_login_url = 'http://esportscomm.coloradocollege.edu/login/cas' # Update this with your Flask app's URL

cas_client = CASClient(cas_url, service_url=app_login_url)

admin_whitelist = ['s_blanchard@coloradocollege.edu', 'jlauer2023@coloradocollege.edu']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(cas_client.get_login_url())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(cas_client.get_logout_url())

@app.route('/login/cas')
def cas_login():
    ticket = request.args.get('ticket')
    if ticket:
        try:
            cas_response = cas_client.perform_service_validate(
                ticket=ticket,
                service_url=app_login_url
            )
        except Exception as e:
            print('CAS validation failed:', e)
            return redirect(url_for('root'))
        
        if cas_response and cas_response.success:
            user_email = cas_response.user
            if user_email.lower() in admin_whitelist:
                session['cas'] = {'user': user_email}
                return redirect(url_for('admin'))  # Redirect to admin page if user is in whitelist
            else:
                return redirect(url_for('normal_website'))  # Redirect to normal website if user is not in whitelist
        else:
            print('CAS validation failed:', cas_response)
            return redirect(url_for('root'))
    else:
        return redirect(url_for('root'))

@app.route('/admin')
def admin():
    if 'cas' in session and 'user' in session['cas']:
        user_email = session['cas']['user']
        if user_email.lower() in admin_whitelist:
            return 'Welcome, admin!'
    return redirect(url_for('normal_website'))  # Redirect to normal website if user is not logged in or not in whitelist

@app.route('/')
def normal_website():
    return 'This is the normal website.'

if __name__ == '__main__':
    app.run(debug=True)
