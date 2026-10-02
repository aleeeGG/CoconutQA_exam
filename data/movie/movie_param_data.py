from faker import Faker

from data.genre.genre_data import get_genre_ids

faker = Faker()

test_genre_id, test_second_genre_id = get_genre_ids()

minPrice = faker.random_int(100, 2000)
maxPrice = minPrice * 2

MOVIE_FILTERS = [
    {"minPrice": minPrice, "maxPrice": maxPrice},
    {"locations": faker.random_element(elements=["MSK", "SPB"])},
    {"genreId": test_genre_id}
]
