import pytest
import allure
from models.movie_response_model import MovieResponseModel  # твоя pydantic модель


@pytest.mark.movies
@pytest.mark.regression
@pytest.mark.xfail(reason="BUG: PATCH /movies/{id} возвращает 404 при существующем ID")
@allure.title("Обновление фильма (PATCH /movies/{id})")
def test_update_movie(super_admin, created_movie):
    """
    Обновление фильма.
    Проверяем обновление имени + проверяем что фильм существует в БД.
    """

    movie_id = created_movie["id"]

    with allure.step("Проверяем, что фильм существует через GET"):
        movie_check = super_admin.api.movies_api.get_movie(movie_id)
        assert movie_check.status_code == 200

    with allure.step("Обновляем фильм"):
        res = super_admin.api.movies_api.update_movie(
            movie_id,
            {
                "name": "Updated Movie",
                "description": created_movie["description"],
                "price": created_movie["price"],
                "location": created_movie["location"],
                "imageUrl": created_movie.get("imageUrl"),
                "published": created_movie["published"],
                "genreId": created_movie["genreId"]
            }
        )

    with allure.step("Проверяем ответ API (должна быть модель)"):
        # тут упадёт из-за бага 404, но оставляем для будущего
        movie_data = MovieResponseModel(**res.json())
        assert movie_data.name == "Updated Movie"

    with allure.step("Проверяем данные в БД"):
        db_movie = super_admin.db_helper.get_movie_by_id(movie_id)
        assert db_movie is not None
        assert db_movie.name == "Updated Movie"


@pytest.mark.movies
@pytest.mark.slow
@allure.title("PATCH /movies/{id} - невалидные данные")
def test_update_movie_invalid(super_admin, created_movie):

    res = super_admin.api.movies_api.update_movie(
        created_movie["id"],
        {"price": -100},
        expected_status=400
    )

    assert res.status_code == 400


@pytest.mark.movies
@allure.title("PATCH /movies/{id} - несуществующий фильм")
def test_update_movie_not_found(super_admin):

    res = super_admin.api.movies_api.update_movie(
        999999,
        {"name": "Fail"},
        expected_status=404
    )

    assert res.status_code == 404