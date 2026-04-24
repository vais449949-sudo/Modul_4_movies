import requests

# -------- GET /movies/{id} -------- #


def test_get_movie_by_id(api_manager, created_movie):
    """
    Получение фильма по ID.
    Проверяем, что возвращаемое тело запроса содержит правильный ID фильма.
    """
    res = api_manager.movies_api.get_movie(created_movie["id"])

    assert res.json()["id"] == created_movie["id"], "Movie ID doesn't match"


def test_get_movie_not_found(api_manager):
    """
    Получение несуществующего фильма по ID.
    Проверяем, что запрос на несуществующий фильм возвращает статус 404.
    """
    api_manager.movies_api.get_movie(999999, expected_status=404)