from data.genre.genre_data import get_genre_ids
from utils.data_generator import DataGenerator

test_genre_id, test_second_genre_id = get_genre_ids()

minPrice = DataGenerator.generate_random_price()
maxPrice = minPrice * 2

MOVIE_FILTERS = [
    {"minPrice": minPrice, "maxPrice": maxPrice},
    {"locations": DataGenerator.generate_random_city()},
    {"genreId": test_genre_id}
]
