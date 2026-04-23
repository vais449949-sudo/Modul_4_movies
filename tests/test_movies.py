import requests
from data_generator.data_generator import DataGenerator


# -------- GET /movies -------- #


def test_get_movies(api_manager):
    """
    Получение афиш фильмов.
    Проверяем, что возвращаемое тело запроса содержит список и общее количество фильмов.
    """
    res = api_manager.movies_api.get_movies()
    body = res.json()

    assert "movies" in body, "Movies list is missing in the response"
    assert "count" in body, "Count is missing in the response"


def test_get_movies_with_filters(api_manager):
    """
    Проверка фильтрации и пагинации.
    Проверяем, что фильтрация по параметрам работает корректно.
    """
    res = api_manager.movies_api.get_movies(params={
        "page": 2,
        "pageSize": 5
    })

    body = res.json()

    assert body["page"] == 2, "Page number is incorrect"
    assert body["pageSize"] == 5, "Page size is incorrect"



def test_invalid_price_filter(api_manager):
    """
    Проверка если minPrice больше чем maxPrice.
    Проверяем, что при неверном фильтре по цене возвращается статус 400.
    """
    api_manager.movies_api.get_movies(
        params={"minPrice": 500, "maxPrice": 100},
        expected_status=400
    )


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


# -------- PATCH /movies/{id} -------- #


def test_update_movie(api_manager, created_movie):
    """
    Обновление фильма.
    Проверяем, что при обновлении фильма его имя меняется.
    """
    res = api_manager.movies_api.update_movie(
        created_movie["id"],
        {"name": "Updated Movie"}
    )

    assert res.json()["name"] == "Updated Movie", "Movie name was not updated"


def test_update_movie_invalid(api_manager, created_movie):
    """
    Обновление фильма невалидными данными.
    Проверяем, что при отправке неправильных данных для обновления фильма возвращается статус 400.
    """
    api_manager.movies_api.update_movie(
        created_movie["id"],
        {"price": -100},
        expected_status=400
    )


def test_update_movie_not_found(api_manager):
    """
    Обновление несуществующего фильма.
    Проверяем, что при попытке обновления несуществующего фильма возвращается статус 404.
    """
    api_manager.movies_api.update_movie(
        999999,
        {"name": "Fail"},
        expected_status=404
    )


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