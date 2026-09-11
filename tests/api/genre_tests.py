from config.admin_credentials import SUPER_ADMIN_CREDS


def test_get_genre(api_manager):
    response = api_manager.genre_api.get_genre()


def test_create_genre(api_manager,test_genre):
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    response = api_manager.genre_api.create_genre(test_genre)