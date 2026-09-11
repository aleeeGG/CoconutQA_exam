from config.admin_credentials import SUPER_ADMIN_CREDS


def test_get_movies_without_params(api_manager):
    response = api_manager.movie_api.get_movies()
    data = response.json()
    assert data["movies"]
    assert isinstance(data["movies"], list)


def test_get_movies_with_params(api_manager, test_movie_param):
    response = api_manager.movie_api.get_movies(test_movie_param)
    data = response.json()
    assert data["movies"]
    assert isinstance(data["movies"], list)
    assert data["pageSize"] == len(data["movies"])
    assert data["pageSize"] <= test_movie_param["pageSize"]
    assert data["page"] == test_movie_param["page"]


def test_create_movie(api_manager, test_movie):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    response = api_manager.movie_api.create_movie(test_movie)
    data = response.json()
    assert data["id"]
    assert data["createdAt"]
    assert data["description"] == test_movie["description"]
    assert data["price"] == test_movie["price"]


def test_create_movie_with_wrong_data(api_manager):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    api_manager.movie_api.create_movie("wrong_data", expected_status=400)


def test_create_movie_with_existing_name(api_manager, test_movie):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    api_manager.movie_api.create_movie(test_movie)
    api_manager.movie_api.create_movie(test_movie, expected_status=409)


def test_get_movie(created_movie, api_manager):
    movie_id = created_movie["id"]
    response = api_manager.movie_api.get_movie(movie_id)
    data = response.json()
    assert data["id"] == movie_id
    assert data["createdAt"] == created_movie["createdAt"]
    assert data["description"] == created_movie["description"]


def test_delete_movie(api_manager, created_movie):
    movie_id = created_movie["id"]
    api_manager.movie_api.get_movie(movie_id)
    api_manager.movie_api.delete_movie(movie_id)
    api_manager.movie_api.get_movie(movie_id, expected_status=404)


def test_delete_non_existing_movie(api_manager, deleted_movie):
    movie_id = deleted_movie["id"]
    api_manager.movie_api.get_movie(movie_id, expected_status=404)
    api_manager.movie_api.delete_movie(movie_id, expected_status=404)


def test_update_movie(api_manager, created_movie, test_movie_patch):
    movie_id = created_movie["id"]
    response = api_manager.movie_api.update_movie(movie_id, test_movie_patch)
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
    api_manager.movie_api.update_movie(
        movie_id, "wrong data", expected_status=400
    )


def test_update_non_existing_movie(api_manager, deleted_movie, test_movie_patch):
    movie_id = deleted_movie["id"]
    api_manager.movie_api.update_movie(
        movie_id, test_movie_patch, expected_status=404
    )