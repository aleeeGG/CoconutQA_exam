
def test_register(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    assert response.json()["email"] == test_user["email"]


def test_login(api_manager, test_user, registered_user):
    response = api_manager.auth_api.authenticate(test_user)
    assert response["user"]["email"] == test_user["email"]
    assert response["accessToken"]


def test_logout(api_manager,registered_user, authenticated_user):
    assert "refresh_token" in api_manager.auth_api.session.cookies
    response = api_manager.auth_api.logout_user()
    assert "refresh_token" not in api_manager.auth_api.session.cookies


def test_refresh_token_with_token(api_manager, authenticated_user):
    response = api_manager.auth_api.refresh_token()

