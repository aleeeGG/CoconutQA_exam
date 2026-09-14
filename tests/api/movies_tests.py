from config.admin_credentials import SUPER_ADMIN_CREDS
from data.movie import movie_data
from utils import assertions


def test_get_movies_without_params(api_manager, created_movie):
    response = api_manager.movie_api.get_movies()
    data = response.json()
    assert "movies" in data
    assert isinstance(data["movies"], list)
    assertions.assert_movie_fields(data["movies"][0])
    assert data["movies"]



def test_get_movies_with_params(api_manager, test_movie_param, created_movie):
    response = api_manager.movie_api.get_movies(test_movie_param)
    data = response.json()
    assert "movies" in data
    assert isinstance(data["movies"], list)
    assertions.assert_movie_fields(data["movies"][0])
    assert "pageSize" in data
    assert "page" in data
    assert data["pageSize"] <= test_movie_param["pageSize"]
    assert data["page"] == test_movie_param["page"]


def test_create_movie(api_manager, test_movie):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    response = api_manager.movie_api.create_movie(test_movie)
    data = response.json()
    assertions.assert_movie_fields(data)
    assert data["description"] == test_movie["description"]
    assert data["price"] == test_movie["price"]


def test_create_movie_with_wrong_data(api_manager):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    response = api_manager.movie_api.create_movie(movie_data.get_movie_wrong_payload(), expected_status=400)
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert data["message"] == [
        "Поле name должно быть строкой",
        "Неверная ссылка",
        "Поле price должно быть числом",
        "Поле location должно быть одним из: MSK, SPB",
        "Поле published должно быть булевым значением",
        "Поле genreId должно быть числом"
    ]
    assert "error" in data
    assert data["error"] == "Bad Request"


def test_create_movie_with_existing_name(api_manager, test_movie):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    api_manager.movie_api.create_movie(test_movie)
    response = api_manager.movie_api.create_movie(test_movie, expected_status=409)
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "error" in data
    assert data["message"] == "Фильм с таким названием уже существует"
    assert data["error"] == "Conflict"


def test_get_movie(created_movie, api_manager):
    movie_id = created_movie["id"]
    response = api_manager.movie_api.get_movie(movie_id)
    data = response.json()
    assert isinstance(data, dict)
    assertions.assert_movie_fields(data)
    assert data["id"] == movie_id
    assert data["createdAt"] == created_movie["createdAt"]
    assert data["description"] == created_movie["description"]


def test_delete_movie(api_manager, movie_for_delete):
    movie_id = movie_for_delete["id"]
    response = api_manager.movie_api.delete_movie(movie_id)
    data = response.json()
    api_manager.movie_api.get_movie(movie_id, expected_status=404)
    assert isinstance(data, dict)
    assertions.assert_movie_fields(data)
    assert data["id"] == movie_id
    assert data["name"] == movie_for_delete["name"]
    assert data["description"] == movie_for_delete["description"]
    assert data["price"] == movie_for_delete["price"]


def test_delete_non_existing_movie(api_manager, deleted_movie):
    movie_id = deleted_movie["id"]
    api_manager.movie_api.get_movie(movie_id, expected_status=404)
    response = api_manager.movie_api.delete_movie(movie_id, expected_status=404)
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "error" in data
    assert data["message"] == "Фильм не найден"
    assert data["error"] == "Not Found"


def test_update_movie(api_manager, created_movie, test_movie_patch):
    movie_id = created_movie["id"]
    response = api_manager.movie_api.update_movie(movie_id, test_movie_patch)
    data = response.json()
    assert isinstance(data, dict)
    assertions.assert_movie_fields(data)
    assert data["id"] == movie_id
    assert data["name"] == test_movie_patch["name"]
    assert data["description"] == test_movie_patch["description"]
    assert data["price"] == test_movie_patch["price"]
    assert data["location"] == test_movie_patch["location"]
    response = api_manager.movie_api.get_movie(movie_id)
    data = response.json()
    assert data["id"] == movie_id
    assert data["name"] == test_movie_patch["name"]
    assert data["description"] == test_movie_patch["description"]
    assert data["price"] == test_movie_patch["price"]
    assert data["location"] == test_movie_patch["location"]


def test_update_movie_with_wrong_data(
        api_manager, created_movie, test_movie_patch
):
    movie_id = created_movie["id"]
    response = api_manager.movie_api.update_movie(
        movie_id, movie_data.get_movie_wrong_payload(), expected_status=400
    )
    data = response.json()
    assert "message" in data
    assert isinstance(data, dict)
    assert data["message"] == [
        "Поле name должно быть строкой",
        "price must not be less than 1",
        "Поле price должно быть числом",
        "location must be one of the following values: MSK, SPB",
        "imageUrl must be a URL address",
        "Поле published должно быть булевым значением",
        "genreId must not be less than 1",
        "Поле genreId должно быть числом"
    ]
    assert "error" in data
    assert data["error"] == "Bad Request"


def test_update_non_existing_movie(api_manager, deleted_movie, test_movie_patch):
    movie_id = deleted_movie["id"]
    response = api_manager.movie_api.update_movie(
        movie_id, test_movie_patch, expected_status=404
    )
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "error" in data
    assert data["message"] == "Фильм не найден"
    assert data["error"] == "Not Found"