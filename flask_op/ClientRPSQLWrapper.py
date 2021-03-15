from flask import current_app

from flask_op.models import OidcRP

client1 = OidcRP(
    "clientapp1",
    client_secret="secret1",
    redirect_uris=["http://localhost:5000/test_auth_callback", "http://localhost:5000/callback", "https://localhost.emobix.co.uk:8443/test/a/test_discovery_endpoint/callback"],
    response_types=["code"],
)
client2 = OidcRP(
    "clientapp2",
    client_secret="secret2",
    redirect_uris=["http://localhost:5000/test_auth_callback", "https://localhost.emobix.co.uk:8443/test/a/test_discovery_endpoint/callback"],
    response_types=["code"],
)


class ClientRPSQLWrapper(object):
    """
    Fonctions de l'interface
    """

    def __setitem__(self, key, value):
        # update db
        pass

    def __getitem__(self, key):
        current_app.logger.debug("__getitem__ : %s" % key)
        # find by id
        for rp in self.items():
            if list(rp.keys())[0] == key:
                return rp[key]

    def __delitem__(self, key):
        # delete by id
        pass

    def __contains__(self, key):
        # find if user exists
        return True

    def items(self):
        current_app.logger.debug("items")
        # get all users
        return [client1, client2]

    def pop(self, key, default=None):
        current_app.logger.debug("pop : %s" % key)
        # ???
        pass
