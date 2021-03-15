import datetime
import flask
import logging
from flask import Flask, jsonify

from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_pyoidc.user_session import UserSession


app = Flask(__name__)
# See http://flask.pocoo.org/docs/0.12/config/
app.config.update({'OIDC_REDIRECT_URI': 'http://localhost:5000/callback',
                   'SECRET_KEY': 'dev_key',
                   'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=7).total_seconds(),
                   'DEBUG': True})

ISSUER = 'https://localhost:8000'
CLIENT1 = 'clientapp1'
PROVIDER_NAME = 'flask_op'
auth_params = {'scope': ['openid', 'profile', 'adress']}
PROVIDER_CONFIG = ProviderConfiguration(issuer=ISSUER,
                                        client_metadata=ClientMetadata(CLIENT1, 'secret1'),
                                        auth_request_params=auth_params)
auth = OIDCAuthentication({PROVIDER_NAME: PROVIDER_CONFIG,})


@app.route('/')
@auth.oidc_auth(PROVIDER_NAME)
def login():
    user_session = UserSession(flask.session)
    return jsonify(access_token=user_session.access_token,
                   id_token=user_session.id_token,
                   userinfo=user_session.userinfo)


@app.route('/logout')
@auth.oidc_logout
def logout():
    return "You've been successfully logged out!"


@auth.error_view
def error(error=None, error_description=None):
    return jsonify({'error': error, 'message': error_description})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    auth.init_app(app)
    app.run()
