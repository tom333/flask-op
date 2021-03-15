import logging

from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_pyfile('config.py')
app.debug= True

CONF_URL = 'https://localhost:8000/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='flask_op',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile adress'
    },
    client_id="clientapp1",
    client_secret="secret1"
)


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return oauth.flask_op.authorize_redirect(redirect_uri)


@app.route('/callback')
def callback():
    token = oauth.flask_op.authorize_access_token()
    user = oauth.flask_op.parse_id_token(token)
    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.run()
