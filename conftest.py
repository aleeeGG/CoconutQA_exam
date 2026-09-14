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
    return ApiManager(session)


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
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    response = api_manager.genre_api.create_genre(test_genre)
    return response.json()["id"]


@pytest.fixture
def created_movie(api_manager, test_movie):
    data = api_manager.movie_api.create_movie(test_movie).json()
    yield data
    movie_id = data["id"]
    api_manager.movie_api.delete_movie(movie_id)

@pytest.fixture
def movie_for_delete(api_manager, test_movie):
    return api_manager.movie_api.create_movie(test_movie).json()


@pytest.fixture
def deleted_movie(api_manager, test_movie, movie_for_delete):
    movie_id = movie_for_delete["id"]
    response = api_manager.movie_api.get_movie(movie_id)
    api_manager.movie_api.delete_movie(movie_id)
    return response.json()
