from utils.data_generator import DataGenerator


def get_movie_patch_payload():
    return {
                  "name": DataGenerator.generate_random_name(),
                  "description": DataGenerator.generate_random_description(),
                  "price": DataGenerator.generate_random_price(),
                  "location": DataGenerator.generate_random_city(),
                  "imageUrl": DataGenerator.generate_random_url(),
                  "published": DataGenerator.generate_random_bool()
            }