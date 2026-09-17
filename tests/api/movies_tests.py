import pytest
from data.movie import movie_data
from utils import assertions


def test_get_movies_without_params(api_manager, created_movie):
    response = api_manager.movies_api.get_movies()
    data = response.json()

    assertions.assert_non_empty_field(data.get("movies")[0])
    assert data.get("movies") is not None
    assert isinstance(data.get("movies"), list)



def test_get_movies_with_params(api_manager, test_movie_param, created_movie):
    response = api_manager.movies_api.get_movies(test_movie_param)
    data = response.json()

    assertions.assert_non_empty_field(data.get("movies")[0])
    assert data.get("movies") is not None
    assert data.get("pageSize") is not None
    assert data.get("page") is not None
    assert isinstance(data.get("movies"), list)

    assert data["pageSize"] <= test_movie_param["pageSize"]
    assert data["page"] == test_movie_param["page"]


def test_create_movie(api_manager, test_movie):
    response = api_manager.movies_api.create_movie(test_movie)
    data = response.json()

    assertions.assert_non_empty_field(data)
    assert isinstance(data, dict)

    assert data["description"] == test_movie["description"]
    assert data["price"] == test_movie["price"]


def test_create_movie_with_wrong_data(api_manager):
    response = api_manager.movies_api.create_movie(movie_data.get_movie_wrong_payload(), expected_status=400)
    data = response.json()

    assert data.get("message") is not None
    assert data.get("error") is not None
    assert isinstance(data, dict)

    assert data["message"] == [
        "Поле name должно быть строкой",
        "Неверная ссылка",
        "Поле price должно быть числом",
        "Поле location должно быть одним из: MSK, SPB",
        "Поле published должно быть булевым значением",
        "Поле genreId должно быть числом"
    ]
    assert data["error"] == "Bad Request"


def test_create_movie_with_existing_name(api_manager, test_movie, created_movie):
    response = api_manager.movies_api.create_movie(created_movie, expected_status=409)
    data = response.json()

    assert data.get("message") is not None
    assert data.get("error") is not None
    assert isinstance(data, dict)

    assert data["message"] == "Фильм с таким названием уже существует"
    assert data["error"] == "Conflict"


def test_get_movie(created_movie, api_manager):
    movie_id = created_movie["id"]
    response = api_manager.movies_api.get_movie(movie_id)
    data = response.json()

    assertions.assert_non_empty_field(data)
    assert isinstance(data, dict)

    assert data["id"] == movie_id
    assert data["createdAt"] == created_movie["createdAt"]
    assert data["description"] == created_movie["description"]

@pytest.mark.parametrize("created_movie", [False], indirect=True)
def test_delete_movie(api_manager, created_movie):
    movie_id = created_movie["id"]
    response = api_manager.movies_api.delete_movie(movie_id)
    data = response.json()

    api_manager.movies_api.get_movie(movie_id, expected_status=404)
    assertions.assert_non_empty_field(data)
    assert isinstance(data, dict)

    assert data["id"] == movie_id
    assert data["name"] == created_movie["name"]
    assert data["description"] == created_movie["description"]
    assert data["price"] == created_movie["price"]


def test_delete_non_existing_movie(api_manager):
    movie_id = 99999999
    api_manager.movies_api.get_movie(movie_id, expected_status=404)
    response = api_manager.movies_api.delete_movie(movie_id, expected_status=404)
    data = response.json()

    assert data.get("message") is not None
    assert data.get("error") is not None
    assert isinstance(data, dict)

    assert data["message"] == "Фильм не найден"
    assert data["error"] == "Not Found"


def test_update_movie(api_manager, created_movie, test_movie_patch):
    movie_id = created_movie["id"]
    response = api_manager.movies_api.update_movie(movie_id, test_movie_patch)
    data = response.json()

    assertions.assert_non_empty_field(data)
    assert isinstance(data, dict)

    assert data["id"] == movie_id
    assert data["name"] == test_movie_patch["name"]
    assert data["description"] == test_movie_patch["description"]
    assert data["price"] == test_movie_patch["price"]
    assert data["location"] == test_movie_patch["location"]

    response = api_manager.movies_api.get_movie(movie_id)
    data = response.json()

    assert data["id"] == movie_id
    assert data["name"] == test_movie_patch["name"]
    assert data["description"] == test_movie_patch["description"]
    assert data["price"] == test_movie_patch["price"]
    assert data["location"] == test_movie_patch["location"]


def test_update_movie_with_wrong_data(api_manager, created_movie, test_movie_patch):
    movie_id = created_movie["id"]
    response = api_manager.movies_api.update_movie(
        movie_id, movie_data.get_movie_wrong_payload(), expected_status=400)
    data = response.json()

    assert data.get("message") is not None
    assert data.get("error") is not None
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
    assert data["error"] == "Bad Request"

    response = api_manager.movies_api.get_movie(movie_id)
    data = response.json()

    assert data["id"] == created_movie["id"]
    assert data["name"] == created_movie["name"]
    assert data["description"] == created_movie["description"]
    assert data["price"] == created_movie["price"]
    assert data["location"] == created_movie["location"]


def test_update_non_existing_movie(api_manager, test_movie_patch):
    movie_id = 999999999
    response = api_manager.movies_api.update_movie(
        movie_id, test_movie_patch, expected_status=404)
    data = response.json()

    assert data.get("message") is not None
    assert data.get("error") is not None
    assert isinstance(data, dict)

    assert data["message"] == "Фильм не найден"
    assert data["error"] == "Not Found"