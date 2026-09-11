from utils.data_generator import DataGenerator

def get_genre_payload():
    return {
              "name": DataGenerator.generate_random_name()
            }