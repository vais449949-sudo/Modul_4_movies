import requests
from data_generator.data_generator import DataGenerator

# -------- POST /movies -------- #


def test_create_movie(api_manager):
    """
    Создание фильма.
    Проверяем, что фильм создается с переданными данными.
    """
    payload = DataGenerator.movie()  # Генерация данных для нового фильма
    res = api_manager.movies_api.create_movie(payload)

    assert res.json()["name"] == payload["name"], "Movie name doesn't match"


def test_create_movie_invalid(api_manager):
    """
    Создание фильма с невалидными данными.
    Проверяем, что при неправильных данных для создания фильма возвращается ошибка 400.
    """
    api_manager.movies_api.create_movie(
        {"name": "Only name"},
        expected_status=400
    )
