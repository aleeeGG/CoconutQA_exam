from faker import Faker
import datetime

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        return faker.email()

    @staticmethod
    def generate_random_name():
        return faker.name()

    @staticmethod
    def generate_random_password():
        return faker.password(
            digits=True,
            lower_case=True,
            upper_case=True,
            length=16,
            special_chars=False,
        )

    @staticmethod
    def generate_random_page():
        return faker.random_int(1, 50)

    @staticmethod
    def generate_random_page_size():
        return faker.random_int(1, 10)

    @staticmethod
    def generate_random_url():
        return faker.url()

    @staticmethod
    def generate_random_price():
        return faker.random_int(100, 2000)

    @staticmethod
    def generate_random_description():
        return faker.sentence()

    @staticmethod
    def generate_random_city():
        return faker.random_element(elements=["MSK", "SPB"])

    @staticmethod
    def generate_random_bool():
        return faker.boolean()

    @staticmethod
    def generate_random_rating():
        return Faker().pyfloat(min_value=0, max_value=5, right_digits=1)

    @staticmethod
    def generate_random_id():
        return faker.random_int(1, 1000000)


    @staticmethod
    def generate_user_data() -> dict:
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_movie_data() -> dict:
        from data.movie import movie_param_data
        id = DataGenerator.generate_random_id()
        return {
            'id': id,
            'name': DataGenerator.generate_random_name()+f" {id}",
            'price': DataGenerator.generate_random_price(),
            'description': DataGenerator.generate_random_description(),
            'image_url': "https://image.url",
            'location': DataGenerator.generate_random_city(),
            'published': True,
            'rating': DataGenerator.generate_random_rating(),
            'genre_id': movie_param_data.get_genre_ids()[0],
            'created_at': datetime.datetime.now()
        }