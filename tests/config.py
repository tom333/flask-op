SERVER_NAME = 'test:8000'
SUBJECT_ID_HASH_SALT = "secret_salt"
PREFERRED_URL_SCHEME = 'https'
DEBUG = True
SECRET_KEY = "secret_key"
SESSION_TYPE = 'filesystem'

OIDC_SCOPES_SUPPORTED = ["openid", "profile", "email"]
OIDC_RESPONSE_TYPES_SUPPORTED = ["code", "code id_token", "code token", "code id_token token"]  # code and hybrid
OIDC_RESPONSE_MODES_SUPPORTED = ["query", "fragment"]
OIDC_GRANT_TYPES_SUPPORTED = ["authorization_code", "implicit"]
OIDC_SUBJECT_TYPE_SUPPORTED = ["pairwise"]
OIDC_TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED = ["client_secret_basic", "private_key_jwt"]
OIDC_USERINFO_SIGNING_ALG_VALUES_SUPPORTED = ["RS256"]
OIDC_CLAIMS_PARAMETER_SUPPORTED = True
OIDC_CLAIMS_SUPPORTED = [
    "sub",
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
    "preferred_username",
]

SIGNING_KEY_FILE = "keys/signing_key.pem"
SIGNING_KEY_ALG = "RS256"
SIGNING_KEY_ID = "main_key"
