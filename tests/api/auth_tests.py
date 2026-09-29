
def test_register(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    assert response.json()["email"] == test_user["email"]


def test_login(api_manager, test_user, registered_user):
    response = api_manager.auth_api.authenticate(test_user)
    assert response["user"]["email"] == test_user["email"]
    assert response["accessToken"]


def test_logout(common_user):
    assert "refresh_token" in common_user.api.auth_api.session.cookies
    response = common_user.api.auth_api.logout_user()
    assert "refresh_token" not in common_user.api.auth_api.session.cookies


def test_refresh_token_with_token(api_manager, authenticated_user):
    response = api_manager.auth_api.refresh_token()

