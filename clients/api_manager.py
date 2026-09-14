from clients.auth_api import AuthApi
from clients.genre_api import GenreApi
from clients.movies_api import MoviesApi
from clients.user_api import UserApi

class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.user_api = UserApi(session)
        self.movie_api = MoviesApi(session)
        self.genre_api = GenreApi(session)