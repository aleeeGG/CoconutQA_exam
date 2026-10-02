from faker import Faker
from db_models.genre import GenreDBModel
from db_requester.db_client import get_db_session

faker = Faker()

def get_genre_payload():
    return {
              "name": faker.name()
            }

def get_genre_ids():
    db = get_db_session()
    genres = db.query(GenreDBModel).limit(2).all()

    return genres[0].id, genres[1].id