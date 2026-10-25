from random import randint

from playwright.sync_api import Page

from pages.base_page import BasePage


class CinescopeMoviePage(BasePage):
    def __init__(self, page: Page, movie_id):
        super().__init__(page)
        self.url = f"{self.home_url}movies/{movie_id}"

        self.review_input = '[data-qa-id="movie_review_input"]'
        self.submit_button = '[data-qa-id="movie_review_submit_button"]'
        self.score_combobox = '[data-qa-id="movie_rating_select"]'
        self.score_value = randint(1, 5)
        self.score = page.get_by_role("option", name=f"{self.score_value}")


    def open(self):
        self.open_url(self.url)

    def create_review(self, text_review: str):
        self.enter_text(self.review_input, text_review)
        self.click(self.score_combobox)
        self.click(self.score)
        self.click(self.submit_button)