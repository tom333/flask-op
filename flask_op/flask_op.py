import logging

from flask import Flask, url_for, jsonify
from jwkest.jwk import RSAKey, rsa_load
from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.subject_identifier import HashBasedSubjectIdentifierFactory
from pyop.userinfo import Userinfo


def init_oidc_provider(app):
    with app.app_context():
        issuer = url_for('oidc_provider.index')[:-1]
        authentication_endpoint = url_for('oidc_provider.authentication_endpoint')
        jwks_uri = url_for('oidc_provider.jwks_uri')
        token_endpoint = url_for('oidc_provider.token_endpoint')
        userinfo_endpoint = url_for('oidc_provider.userinfo_endpoint')
        registration_endpoint = url_for('oidc_provider.registration_endpoint')
        end_session_endpoint = url_for('oidc_provider.end_session_endpoint')

    configuration_information = {
        'issuer': issuer,
        'authorization_endpoint': authentication_endpoint,
        'jwks_uri': jwks_uri,
        'token_endpoint': token_endpoint,
        'userinfo_endpoint': userinfo_endpoint,
        'registration_endpoint': registration_endpoint,
        'end_session_endpoint': end_session_endpoint,
        'scopes_supported': ['openid', 'profile', 'email'],
        'response_types_supported': ['code', 'code id_token', 'code token', 'code id_token token'],  # code and hybrid
        'response_modes_supported': ['query', 'fragment'],
        'grant_types_supported': ['authorization_code', 'implicit'],
        'subject_types_supported': ['pairwise'],
        'token_endpoint_auth_methods_supported': ['client_secret_basic', 'private_key_jwt'],
        'claims_parameter_supported': True,
        'claims_supported': ["sub",
                              "name",
                              "given_name",
                              "family_name",
                              "middle_name",
                              "nickname",
                              "profile",
                              "picture",
                              "website",
                              "gender",
                              "birthdate",
                              "zoneinfo",
                              "locale",
                              "updated_at",
                              "preferred_username"],
    }
    clients = {
        "clientapp1": {
            "client_secret": "secret1",
            "redirect_uris": ["http://localhost:5000/test_auth_callback", "https://localhost.emobix.co.uk:8443/test/a/test_discovery_endpoint/callback"],
            "response_types": ["code"],
        },

        "clientapp2": {
            "client_secret": "secret2",
            "redirect_uris": ["http://localhost:5000/test_auth_callback", "https://localhost.emobix.co.uk:8443/test/a/test_discovery_endpoint/callback"],
            "response_types": ["code"],
        }
    }

    userinfo_db = Userinfo(app.users)
    signing_key = RSAKey(key=rsa_load('keys/signing_key.pem'), alg='RS256', kid="toto")
    provider = Provider(signing_key, configuration_information,
                        AuthorizationState(HashBasedSubjectIdentifierFactory(app.config['SUBJECT_ID_HASH_SALT'])),
                        clients, userinfo_db)

    return provider


def create_app(config_file):
    app = Flask("flask_op")
    app.config.from_pyfile(config_file)
    app.users = {'test_user': {'name': 'Testing Name', "website": "None",
              "zoneinfo": "None",
              "birthdate": "2000-01-01",
              "gender": "None",
              "profile": "None",
              "preferred_username": "None",
              "given_name": "None",
              "middle_name": "None",
              "locale": "None",
              "picture": "None",
              "updated_at": 1615351682,
              "nickname": "None",
              "family_name": "None",
              "email_verified": True,
              "email": "test@test.com"
                               }}

    from flask_op.views.oidc import oidc_provider_views
    app.register_blueprint(oidc_provider_views)

    # Initialize the oidc_provider after views to be able to set correct urls
    app.provider = init_oidc_provider(app)
    app.logger.error(app.url_map)

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = create_app("config.py")
    app.run()