import pytest

from playwright.sync_api import Page

from config.base_urls import HOME_BASE_URL
from pages.login_page import CinescopeLoginPage
from pages.movie_page import CinescopeMoviePage
from pages.register_page import CinescopeRegisterPage
from tests.ui.common.tools import Tools

DEFAULT_UI_TIMEOUT = 30000

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def register_page(page: Page) -> CinescopeRegisterPage:
    register_page = CinescopeRegisterPage(page)
    register_page.open()
    return register_page

@pytest.fixture
def login_page(page: Page) -> CinescopeLoginPage:
    login_page = CinescopeLoginPage(page)
    login_page.open()
    return login_page

@pytest.fixture
def movie_page(page: Page, created_test_movie) -> CinescopeMoviePage:
    movie_page = CinescopeMoviePage(page, created_test_movie.id)
    movie_page.open()
    return movie_page

@pytest.fixture
def authorization(page: Page, login_page, common_user):
    login_page.login(common_user.email, common_user.password)
    page.wait_for_timeout(1000)
    page.reload()
    page.wait_for_url(HOME_BASE_URL)
    assert page.url == HOME_BASE_URL
    return common_user

