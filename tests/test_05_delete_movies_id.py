import requests
from data_generator.data_generator import DataGenerator


# -------- DELETE /movies/{id} -------- #


def test_delete_movie(api_manager):
    """
    Удаление фильма.
    Проверяем, что фильм удаляется.
    """
    movie = api_manager.movies_api.create_movie(
        DataGenerator.movie()
    ).json()

    api_manager.movies_api.delete_movie(movie["id"])


def test_delete_movie_not_found(api_manager):
    """
    Удаление несуществующего фильма.
    Проверяем, что удаление несуществующего фильма возвращает статус 404.
    """
    api_manager.movies_api.delete_movie(
        999999,
        expected_status=404
    )