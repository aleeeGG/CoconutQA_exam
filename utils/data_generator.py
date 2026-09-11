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
