import requests

from config.base_urls import MOVIES_BASE_URL
from db_models.genre import GenreDBModel
from db_requester.db_client import get_db_session
from utils.data_generator import DataGenerator

def get_genre_payload():
    return {
              "name": DataGenerator.generate_random_name()
            }

def get_genre_ids():
    db = get_db_session()
    genres = db.query(GenreDBModel).limit(2).all()

    return genres[0].id, genres[1].id
    #моя жалкая попытка избавиться от хардкода