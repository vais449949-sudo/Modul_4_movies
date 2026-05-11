import pytest
import allure
from data_generator.data_generator import DataGenerator


# -------- DELETE /movies/{id} -------- #

@pytest.mark.movies
@pytest.mark.smoke
@allure.title("Удаление фильма")
def test_delete_movie(super_admin):

    movie = super_admin.api.movies_api.create_movie(
        DataGenerator.movie()
    ).json()

    movie_id = movie["id"]

    super_admin.api.movies_api.delete_movie(movie_id)

    res = super_admin.api.movies_api.get_movie(
        movie_id,
        expected_status=404
    )

    assert res.status_code == 404


@pytest.mark.movies
@pytest.mark.negative
@allure.title("Удаление несуществующего фильма")
def test_delete_movie_not_found(super_admin):

    res = super_admin.api.movies_api.delete_movie(
        999999,
        expected_status=404
    )

    assert res.status_code == 404