import requests

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
