import allure
import pytest
from playwright.sync_api import expect

from tests.ui.conftest import page
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Отзывы")
@pytest.mark.ui
class TestReview:
    @allure.title("Успешное создание отзыва")
    def test_review(self,authorization, movie_page, page, created_test_movie):
        review = DataGenerator.generate_random_description()
        movie_page.create_review(review)
        notification = page.get_by_role("status")
        expect(notification).to_be_visible()
        expect(notification).to_contain_text("Отзыв успешно создан")
        reviewer = page.locator("h4")
        expect(reviewer).to_contain_text(authorization.full_name)
        expect(reviewer).to_be_visible()
        expect(page.get_by_text(f"{review}")).to_be_visible()
        review_block = page.locator(".rounded-xl").filter(has_text=review)
        expect(review_block).to_contain_text(f"{movie_page.score_value}/5")
        expect(review_block).to_be_visible()