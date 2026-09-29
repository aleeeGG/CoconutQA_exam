from clients.api_manager import ApiManager

class User:
    def __init__(self, email: str, password: str, api: ApiManager):
        self.email = email
        self.password = password
        self.api = api

    @property
    def creds(self):
        return self.email, self.password