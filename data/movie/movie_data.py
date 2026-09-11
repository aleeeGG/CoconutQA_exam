from utils.data_generator import DataGenerator

def get_movie_payload(genre_id):
    return {
              "name": DataGenerator.generate_random_name(),
              "imageUrl": DataGenerator.generate_random_url(),
              "price": DataGenerator.generate_random_price(),
              "description": DataGenerator.generate_random_description(),
              "location": DataGenerator.generate_random_city(),
              "published": DataGenerator.generate_random_bool(),
              "genreId": genre_id
            }