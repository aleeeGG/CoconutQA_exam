from faker import Faker

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
        return faker.random_int(1, 10)

    @staticmethod
    def generate_random_page_size():
        return faker.random_int(1, 10)

    @staticmethod
    def generate_random_url():
        return faker.url()

    @staticmethod
    def generate_random_price():
        return faker.random_int(100, 5000)

    @staticmethod
    def generate_random_description():
        return faker.sentence()

    @staticmethod
    def generate_random_city():
        return faker.random_element(elements=["MSK", "SPB"])

    @staticmethod
    def generate_random_bool():
        return faker.boolean()
