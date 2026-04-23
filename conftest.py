import pytest
import requests

from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager
from constants import AUTH_BASE_URL, MOVIES_BASE_URL
from clients.auth_api import AuthAPI



@pytest.fixture
def api_manager():
    session = requests.Session()

    # Requester для авторизации
    auth_requester = CustomRequester(session, AUTH_BASE_URL)
    # Requester для фильмов
    movies_requester = CustomRequester(session, MOVIES_BASE_URL)

    api = ApiManager(auth_requester, movies_requester)

    # Авторизуемся с заранее заданными данными
    api.authenticate("api1@gmail.com", "asdqwe123Q")

    return api

@pytest.fixture
def created_movie(api_manager):
    from data_generator.data_generator import DataGenerator

    movie = api_manager.movies_api.create_movie(
        DataGenerator.movie()
    ).json()

    yield movie

    api_manager.movies_api.delete_movie(movie["id"])