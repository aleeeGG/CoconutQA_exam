import pytest
import requests

from clients.api_manager import ApiManager
from config.admin_credentials import SUPER_ADMIN_CREDS
from data.auth import register_data
from data.genre import genre_data
from data.movie import movie_data, movie_param_data, movie_patch_data


@pytest.fixture(scope="session")
def session():
    return requests.Session()


@pytest.fixture
def test_user():
    return register_data.get_register_payload()


@pytest.fixture(scope="session")
def api_manager(session):
    api_manager = ApiManager(session)
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    return api_manager


@pytest.fixture
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    return response.json()


@pytest.fixture(scope="session")
def unauthenticated_api_manager():
    session = requests.Session()
    yield ApiManager(session)
    session.close()


@pytest.fixture
def authenticated_user(api_manager, test_user, registered_user):
    user_data = registered_user
    api_manager.auth_api.authenticate(test_user)
    return user_data


@pytest.fixture
def test_movie(genre_id):
    return movie_data.get_movie_payload(genre_id)


@pytest.fixture
def test_movie_param():
    return movie_param_data.get_movie_param()


@pytest.fixture
def test_genre():
    return genre_data.get_genre_payload()


@pytest.fixture
def test_movie_patch():
    return movie_patch_data.get_movie_patch_payload()


@pytest.fixture
def genre_id(api_manager, test_genre):
    response = api_manager.genre_api.create_genre(test_genre)
    return response.json()["id"]


@pytest.fixture
def created_movie(api_manager, test_movie, request):
    response = api_manager.movies_api.create_movie(test_movie)
    movie = response.json()

    yield movie

    if not getattr(request, "param", True):
        return

    api_manager.movies_api.delete_movie(movie["id"])
