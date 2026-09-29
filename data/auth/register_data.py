from constants.roles import Roles
from utils.data_generator import DataGenerator

def get_register_payload():
    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": [Roles.USER.value] # Это поле ни на что не влияет, всегда создается юзер
    }