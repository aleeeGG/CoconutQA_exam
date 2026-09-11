import pytest
import requests

from clients.api_manager import ApiManager
from data.auth import register_data

@pytest.fixture(scope="session")
def session():
    return requests.Session()

@pytest.fixture
def test_user():
    return register_data.get_register_payload()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

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
