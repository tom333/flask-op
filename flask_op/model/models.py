class User(dict):
    def __init__(self, login) -> None:
        super().__init__()
        self.update(
            {
                "login": login,
                "sub": "1",
                "name": "Testing Name",
                "website": "None",
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
                "email": "test@test.com",
            }
        )


class OidcRP(dict):
    def __init__(self, client_id, client_secret=None, redirect_uris=[], response_types=[]) -> None:
        super().__init__()
        self.update(
            {
                client_id: {
                    "client_secret": client_secret,
                    "redirect_uris": redirect_uris,
                    "response_types": response_types,
                }
            }
        )
