import allure
import pytest

from conftest import created_test_movie
from data.movie import movie_data
from data.movie.movie_param_data import MOVIE_FILTERS

from models.base_models import Movie, MoviesPage
import logging
logger = logging.getLogger(__name__)


@allure.epic("Тестирование Cinescope")
@allure.feature("Тестирование Movies")
class TestMovie:

    @allure.title("Тест get запроса списка фильмов без параметров")
    @pytest.mark.positive
    def test_get_movies_without_params(self, api_manager, created_test_movie):
        response = api_manager.movies_api.get_movies()
        movie = MoviesPage(**response.json())
        assert movie.movies

    @allure.title("Тест get запроса списка фильмов с параметрами")
    @pytest.mark.positive
    @pytest.mark.parametrize("movie_filter", MOVIE_FILTERS)
    def test_get_movies_with_params(self, api_manager, movie_filter, create_films_for_filters):
        response = api_manager.movies_api.get_movies(movie_filter)
        movies = MoviesPage(**response.json())

        for movie in movies.movies:
            if "genreId" in movie_filter:
                with allure.step("Проверка фильтра genreId"):
                    assert movie.genreId == movie_filter["genreId"]

            if "location" in movie_filter:
                with allure.step("Проверка фильтра location"):
                    assert movie.location == movie_filter["location"]

            if "minPrice" in movie_filter:
                with allure.step("Проверка фильтра price"):
                    assert movie.price >= movie_filter["minPrice"]
                    assert movie.price <= movie_filter["maxPrice"]


    @allure.title("Тест создания фильма")
    @pytest.mark.positive
    def test_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movies_api.create_movie(test_movie)
        movie = Movie(**response.json())

        assert movie.name == test_movie["name"]
        assert movie.genreId == test_movie["genreId"]
        assert movie.location == test_movie["location"]
        assert movie.description == test_movie["description"]
        assert movie.price == test_movie["price"]
        assert movie.published == test_movie["published"]
        assert movie.imageUrl == test_movie["imageUrl"]


    @allure.title("Попытка создать фильм с неправильными данными")
    @pytest.mark.negative
    def test_create_movie_with_wrong_data(self, super_admin):
        response = super_admin.api.movies_api.create_movie(movie_data.get_movie_wrong_payload(), expected_status=400)
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


    @allure.title("Попытка создать фильм с существующим именем")
    @pytest.mark.negative
    def test_create_movie_with_existing_name(self, super_admin, test_movie, created_test_movie):
        test_movie['name'] = created_test_movie.name
        response = super_admin.api.movies_api.create_movie(test_movie, expected_status=409)
        data = response.json()

        assert data.get("message") is not None
        assert data.get("error") is not None
        assert isinstance(data, dict)

        assert data["message"] == "Фильм с таким названием уже существует"
        assert data["error"] == "Conflict"


    @allure.title("Тест get запроса по id фильма")
    @pytest.mark.positive
    def test_get_movie(self, created_test_movie, api_manager):
        response = api_manager.movies_api.get_movie(created_test_movie.id)
        movie = Movie(**response.json())

        assert movie.id == created_test_movie.id
        # assert movie.createdAt == created_test_movie.created_at
        # БД возвращает формат даты и времени отличный от АПИ, я бы сказал, что баг
        assert movie.description == created_test_movie.description
        assert movie.genreId == created_test_movie.genre_id
        assert movie.location == created_test_movie.location
        assert movie.imageUrl == created_test_movie.image_url
        assert movie.published == created_test_movie.published
        assert movie.price == created_test_movie.price
        assert movie.name == created_test_movie.name
        assert movie.rating == created_test_movie.rating


    @allure.title("Тест удаления фильма")
    @pytest.mark.positive
    @pytest.mark.parametrize("created_test_movie", [False], indirect=True)
    def test_delete_movie(self, super_admin, created_test_movie, db_helper):
        with allure.step("Проверить наличие фильма в БД"):
            assert db_helper.get_movie_by_id(created_test_movie.id)

        with allure.step("Удалить фильм от имени super_admin"):
            response = super_admin.api.movies_api.delete_movie(
                created_test_movie.id,
                expected_status=200
            )

        movie = Movie(**response.json())

        with allure.step("Проверить удаление фильма из БД"):
            assert db_helper.get_movie_by_id(created_test_movie.id) is None

        assert movie.id == created_test_movie.id
        assert movie.name == created_test_movie.name
        assert movie.description == created_test_movie.description
        assert movie.price == created_test_movie.price


    @allure.title("Попытка удаления фильма без прав")
    @pytest.mark.negative
    @pytest.mark.parametrize("created_test_movie", [False], indirect=True)
    @pytest.mark.parametrize("role", ["admin", "common_user"])
    def test_delete_movie_without_permission(self, request, role, created_test_movie, db_helper):
        with allure.step("Проверить наличие фильма в БД"):
            assert db_helper.get_movie_by_id(created_test_movie.id)

        users = {
            "admin": ("admin", 403),
            "common_user": ("common_user", 403)
        }

        fixture_name, expected_status = users[role]
        user = request.getfixturevalue(fixture_name)

        with allure.step(f"Удалить фильм от имени {role}"):
            user.api.movies_api.delete_movie(
                created_test_movie.id,
                expected_status=expected_status
            )

            movie = db_helper.get_movie_by_id(created_test_movie.id)

        with allure.step("Проверить, что фильм не удалён"):
            assert movie.name == created_test_movie.name
            assert movie.description == created_test_movie.description
            assert movie.price == created_test_movie.price


    @allure.title("Попытка удалить несуществующий фильм")
    @pytest.mark.negative
    @pytest.mark.flaky(reruns=3)
    def test_delete_non_existing_movie(self, super_admin, db_helper):
        movie_id = 99999999
        with allure.step("Проверка что фильм действительно не существует"):
            assert db_helper.get_movie_by_id(movie_id) is None
        with allure.step("Попытка удаления"):
            response = super_admin.api.movies_api.delete_movie(movie_id, expected_status=404)
        data = response.json()

        assert data.get("message") is not None
        assert isinstance(data, dict)

        assert data["message"] == "Фильм не найден"
        assert data["error"] == "Not Found"

        with allure.step("Проверка что фильма нет в БД после удаления"):
            assert db_helper.get_movie_by_id(movie_id) is None


    @allure.title("Тест обновления фильма")
    @pytest.mark.positive
    def test_update_movie(self, super_admin, created_test_movie, test_movie_patch, db_helper):
        with allure.step("Обновление фильма"):
            response = super_admin.api.movies_api.update_movie(created_test_movie.id, test_movie_patch)
        movie = Movie(**response.json())

        assert movie.id == created_test_movie.id
        assert movie.name == test_movie_patch["name"]
        assert movie.description == test_movie_patch["description"]
        assert movie.price == test_movie_patch["price"]
        assert movie.location == test_movie_patch["location"]
        assert movie.imageUrl == test_movie_patch["imageUrl"]
        assert movie.published == test_movie_patch["published"]


        movie = db_helper.get_movie_by_id(created_test_movie.id)
        with allure.step("Проверка что фильм действительно обновлен"):
            assert movie.name == test_movie_patch["name"]
            assert movie.description == test_movie_patch["description"]
            assert movie.price == test_movie_patch["price"]
            assert movie.location == test_movie_patch["location"]


    @allure.title("Попытка обновить фильм с неправильными данными")
    @pytest.mark.negative
    def test_update_movie_with_wrong_data(self, super_admin, created_test_movie, test_movie_patch, db_helper):
        movie_id = created_test_movie.id
        with allure.step("Попытка обновления"):
            response = super_admin.api.movies_api.update_movie(
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

        movie = db_helper.get_movie_by_id(movie_id)
        with allure.step("Проверка что фильм не обновлен"):
            assert movie.name == created_test_movie.name
            assert movie.description == created_test_movie.description
            assert movie.price == created_test_movie.price
            assert movie.location == created_test_movie.location


    @allure.title("Попытка обновления несуществующего фильма")
    @pytest.mark.negative
    def test_update_non_existing_movie(self, super_admin, test_movie_patch):
        movie_id = 999999999
        response = super_admin.api.movies_api.update_movie(
            movie_id, test_movie_patch, expected_status=404)
        data = response.json()

        assert data.get("message") is not None
        assert data.get("error") is not None
        assert isinstance(data, dict)

        assert data["message"] == "Фильм не найден"
        assert data["error"] == "Not Found"