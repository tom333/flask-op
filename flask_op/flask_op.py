import logging

from flask import Flask, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_session import Session
from jwkest.jwk import RSAKey, rsa_load
from pyop.authz_state import AuthorizationState
from pyop.provider import Provider
from pyop.subject_identifier import HashBasedSubjectIdentifierFactory
from pyop.userinfo import Userinfo

from flask_op.model import ClientRPSQLWrapper, UserSQLWrapper


def init_oidc_provider(app):
    with app.app_context():
        issuer = url_for("oidc_provider.index")[:-1]
        authentication_endpoint = url_for("oidc_provider.authentication_endpoint")
        jwks_uri = url_for("oidc_provider.jwks_uri")
        token_endpoint = url_for("oidc_provider.token_endpoint")
        userinfo_endpoint = url_for("oidc_provider.userinfo_endpoint")
        registration_endpoint = url_for("oidc_provider.registration_endpoint")
        end_session_endpoint = url_for("oidc_provider.end_session_endpoint")

    configuration_information = {
        "issuer": issuer,
        "authorization_endpoint": authentication_endpoint,
        "jwks_uri": jwks_uri,
        "token_endpoint": token_endpoint,
        "userinfo_endpoint": userinfo_endpoint,
        "registration_endpoint": registration_endpoint,
        "end_session_endpoint": end_session_endpoint,
        "scopes_supported": app.config["OIDC_SCOPES_SUPPORTED"],
        "response_types_supported": app.config["OIDC_RESPONSE_TYPES_SUPPORTED"],
        "response_modes_supported": app.config["OIDC_RESPONSE_MODES_SUPPORTED"],
        "grant_types_supported": app.config["OIDC_GRANT_TYPES_SUPPORTED"],
        "subject_types_supported": app.config["OIDC_SUBJECT_TYPE_SUPPORTED"],
        "token_endpoint_auth_methods_supported": app.config["OIDC_TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED"],
        "userinfo_signing_alg_values_supported": app.config["OIDC_USERINFO_SIGNING_ALG_VALUES_SUPPORTED"],
        "claims_parameter_supported": app.config["OIDC_CLAIMS_PARAMETER_SUPPORTED"],
        "claims_supported": app.config["OIDC_CLAIMS_SUPPORTED"],
    }

    userinfo_db = Userinfo(app.sql_backend)
    signing_key = RSAKey(key=rsa_load(app.config["SIGNING_KEY_FILE"]), alg=app.config["SIGNING_KEY_ALG"], kid=app.config["SIGNING_KEY_ID"])
    provider = Provider(
        signing_key,
        configuration_information,
        AuthorizationState(HashBasedSubjectIdentifierFactory(app.config["SUBJECT_ID_HASH_SALT"])),
        ClientRPSQLWrapper(),
        userinfo_db,
    )

    return provider


def create_app(config_file):
    app = Flask("flask_op")
    app.config.from_pyfile(config_file)

    from flask_op.views import oidc_provider_views

    app.register_blueprint(oidc_provider_views)

    sess = Session()
    sess.init_app(app)

    sql_backend = UserSQLWrapper()
    sql_backend.init_app(app)

    # Initialize the oidc_provider after views to be able to set correct urls
    app.provider = init_oidc_provider(app)
    app.logger.error(app.url_map)

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    flask_op_app = create_app("config.py")
    flask_op_app.run()
