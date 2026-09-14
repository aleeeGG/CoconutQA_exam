from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

GENRE = '/genres'


class GenreApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_genre(self, params = None, expected_status = 200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=GENRE,
            params=params,
            expected_status=expected_status,
            **kwargs
        )
    def create_genre(self,genre_data, expected_status = 201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=GENRE,
            data=genre_data,
            expected_status=expected_status,
            **kwargs
        )