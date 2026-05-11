import requests

import pytest
import allure

from models.movie_response_model import MovieResponseModel


# -------- GET /movies/{id} -------- #

@pytest.mark.movies
@pytest.mark.smoke
@allure.title("Получение фильма по ID")
def test_get_movie_by_id(unauthorized_api, created_movie):

    res = unauthorized_api.movies_api.get_movie(created_movie["id"])
    body = MovieResponseModel(**res.json())

    assert body.id == created_movie["id"]
    assert body.name == created_movie["name"]


@pytest.mark.movies
@pytest.mark.negative
@allure.title("Получение несуществующего фильма")
def test_get_movie_not_found(unauthorized_api):

    res = unauthorized_api.movies_api.get_movie(999999, expected_status=404)

    assert res.status_code == 404