from config.admin_credentials import SUPER_ADMIN_CREDS


def test_get_genre(api_manager):
    response = api_manager.genre_api.get_genre()
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert "id" in data[0]
    assert "name" in data[0]

def test_create_genre(api_manager, test_genre):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)

    response = api_manager.genre_api.create_genre(test_genre)
    data = response.json()

    assert response.status_code == 201
    assert isinstance(data, dict)
    assert "id" in data
    assert "name" in data
    assert data["name"] == test_genre["name"]