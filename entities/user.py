from clients.api_manager import ApiManager

class User:
    def __init__(self, email: str, password: str, api: ApiManager, full_name: str = None):
        self.email = email
        self.password = password
        self.api = api
        self.full_name = full_name

    @property
    def creds(self):
        return self.email, self.password