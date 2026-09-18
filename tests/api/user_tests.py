from config.admin_credentials import SUPER_ADMIN_CREDS
from data.auth import register_data


def test_get_user_info_auth_admin(api_manager, test_user, registered_user):
    user_id = registered_user["id"]
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    response = api_manager.user_api.get_user_info(user_id)
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == test_user["email"]


def test_get_user_info_auth_user(api_manager, test_user, registered_user):
    user_id = registered_user["id"]
    api_manager.auth_api.authenticate(test_user)
    api_manager.user_api.get_user_info(user_id, expected_status=403)


def test_get_user_info_not_auth(unauthenticated_api_manager, registered_user):
    user_id = registered_user["id"]
    unauthenticated_api_manager.user_api.get_user_info(user_id, expected_status=401)


def test_delete_three_users(api_manager, test_user):
    user1 = register_data.get_register_payload()
    user2 = register_data.get_register_payload()
    user3 = register_data.get_register_payload()

    user_id1 = api_manager.auth_api.register_user(user1).json()["id"]
    user_id2 = api_manager.auth_api.register_user(user2).json()["id"]
    user_id3 = api_manager.auth_api.register_user(user3).json()["id"]

    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    api_manager.user_api.delete_users(user_id1, user_id2, user_id3, expected_status=200)