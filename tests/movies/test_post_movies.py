import requests
import allure
import pytest
from data_generator.data_generator import DataGenerator
from models.movie_response_model import MovieResponseModel

# -------- POST /movies -------- #

@pytest.mark.movies
@pytest.mark.smoke
@allure.title("Создание фильма")
def test_create_movie(super_admin):

    payload = DataGenerator.movie()

    res = super_admin.api.movies_api.create_movie(payload)
    body = MovieResponseModel(**res.json())

    assert body.name == payload["name"]
    assert body.price == payload["price"]
    assert body.description == payload["description"]
    assert body.location == payload["location"]


@pytest.mark.movies
@pytest.mark.negative
@allure.title("Создание фильма с невалидными данными")
def test_create_movie_invalid(super_admin):

    res = super_admin.api.movies_api.create_movie(
        {"name": "Only name"},
        expected_status=400
    )

    assert res.status_code == 400

@pytest.mark.movies
@pytest.mark.db
@allure.title("Создание фильма + проверка в БД")
def test_create_movie_db(super_admin):

    payload = DataGenerator.movie()

    res = super_admin.api.movies_api.create_movie(payload)
    body = MovieResponseModel(**res.json())

    movie_id = body.id

    # --- проверка API ---
    assert body.name == payload["name"]
    assert body.price == payload["price"]
    assert body.description == payload["description"]
    assert body.location == payload["location"]

    # --- проверка БД ---
    db_movie = super_admin.db_helper.get_movie_by_id(movie_id)

    assert db_movie is not None
    assert db_movie.name == payload["name"]
    assert db_movie.price == payload["price"]