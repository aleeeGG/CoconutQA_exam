from utils.data_generator import DataGenerator

def get_movie_param():
    return {
        "pageSize": DataGenerator.generate_random_page_size(),
        "page": DataGenerator.generate_random_page(),
    }