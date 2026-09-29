import pytest
import requests

from clients.api_manager import ApiManager
from config.admin_credentials import SuperAdminCreds
from constants.roles import Roles
from data.auth import register_data
from data.genre import genre_data
from data.movie import movie_data, movie_param_data, movie_patch_data
from entities.user import User
from models.base_models import Movie, MovieCreateModel, MoviePatchModel
from utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper

@pytest.fixture(scope="session")
def session():
    return requests.Session()


@pytest.fixture
def test_user():
    return register_data.get_register_payload()


@pytest.fixture(scope="session")
def api_manager(session):
    api_manager = ApiManager(session)
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
    data = movie_data.get_movie_payload(genre_id)
    MovieCreateModel(**data)
    return data


@pytest.fixture
def test_genre():
    return genre_data.get_genre_payload()


@pytest.fixture
def test_movie_patch():
    data = movie_patch_data.get_movie_patch_payload()
    MoviePatchModel(**data)
    return data


@pytest.fixture
def genre_id(db_helper):
    return db_helper.get_first_genre().id



@pytest.fixture
def created_movie(super_admin, test_movie, request):
    response = super_admin.api.movies_api.create_movie(test_movie)
    movie = Movie(**response.json())

    yield movie

    if not getattr(request, "param", True):
        return

    super_admin.api.movies_api.delete_movie(movie.id)

@pytest.fixture
def created_user(creation_user_data, super_admin):
    created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
    yield created_user_response
    super_admin.api.user_api.delete_user(created_user_response["id"])

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
            "verified": True,
            "banned": False
        })
    return updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        new_session)

    response = super_admin.api.user_api.create_user(creation_user_data)
    admin_id = response.json()["id"]

    admin_data = {
        "roles": [Roles.ADMIN.value]
    }

    super_admin.api.user_api.patch_user(admin_id, admin_data) #Знаю, что костыль, но сразу админа не создать, объяснил в data/auth/register_data

    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture
def create_films_for_filters(db_helper):
    # подходящий под фильтры фильм
    movie_data = DataGenerator.generate_movie_data()

    movie_data["name"] = DataGenerator.generate_random_name()
    movie_data['price'] = (movie_param_data.MOVIE_FILTERS[0]["minPrice"] +
                           movie_param_data.MOVIE_FILTERS[0]["maxPrice"])/2
    movie_data['location'] = movie_param_data.MOVIE_FILTERS[1]["locations"]
    movie_data['genre_id'] = movie_param_data.MOVIE_FILTERS[2]["genreId"]

    data = db_helper.create_test_movie(movie_data)

    # неподходящий под фильтры фильм
    movie_data = DataGenerator.generate_movie_data()

    movie_data["name"] = DataGenerator.generate_random_name()
    movie_data['price'] = movie_param_data.MOVIE_FILTERS[0]["maxPrice"] + 100
    if movie_data['location'] == "MSK":
        movie_data['location'] = "SPB"
    else:
        movie_data['location'] = "MSK"
    movie_data['genre_id'] = movie_param_data.test_second_genre_id

    second_data = db_helper.create_test_movie(movie_data)

    yield data
    db_helper.delete_movie(data)
    db_helper.delete_movie(second_data)


@pytest.fixture(scope="module")
def db_session() -> Session:
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def created_test_movie(db_helper):
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    yield movie
    if db_helper.get_movie_by_id(movie.id):
        db_helper.delete_movie(movie)