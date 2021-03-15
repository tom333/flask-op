from flask_op.views import oidc

from flask_op.views.oidc import (authentication_endpoint, consent, do_logout,
                                 end_session_endpoint, index, jwks_uri,
                                 log_request, log_request_info, log_user,
                                 oidc_provider_views, provider_configuration,
                                 registration_endpoint, token_endpoint,
                                 userinfo_endpoint,)

__all__ = ['authentication_endpoint', 'consent', 'do_logout',
           'end_session_endpoint', 'index', 'jwks_uri', 'log_request',
           'log_request_info', 'log_user', 'oidc', 'oidc_provider_views',
           'provider_configuration', 'registration_endpoint', 'token_endpoint',
           'userinfo_endpoint']
