import pytest
import allure

from config.base_urls import HOME_BASE_URL


@allure.epic("Тестирование UI")
@allure.feature("Авторизация")
@pytest.mark.ui
class TestLogin:
    @allure.title("Успешная авторизация нового пользователя")
    def test_login(self, login_page, page, common_user):
        login_page.login(common_user.email, common_user.password)
        page.wait_for_timeout(1000)
        page.reload()
        page.wait_for_url(HOME_BASE_URL)
        assert page.url == HOME_BASE_URL
