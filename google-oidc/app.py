from flask import Flask, redirect, url_for, session, render_template, request, flash
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object('config')

# OAuth configuration
oauth = OAuth(app)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dummy_login', methods=['POST'])
def dummy_login():
    username = request.form['username']
    password = request.form['password']
    # Dummy check for username and password
    if username == 'admin' and password == 'password':
        session['user'] = {'email': 'admin@example.com'}
        return redirect('/profile')
    else:
        flash('Invalid username or password')
        return redirect(url_for('index', error='Invalid username or password'))


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = token['userinfo']
    
    session['user'] = {
        'name': user_info.get('name'),
        'email': user_info.get('email'),
        'given_name': user_info.get('given_name'),
        'family_name': user_info.get('family_name'),
        'picture': user_info.get('picture'),
    }    
    return redirect('/profile')


@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)
    app.run(debug=os.environ.get('FLASK_DEBUG', False), host='0.0.0.0')
