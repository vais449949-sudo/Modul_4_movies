import requests
import allure
import pytest
from models.movie_response_model import MoviesListResponseModel


# -------- GET /movies -------- #

@pytest.mark.movies
@pytest.mark.smoke
@allure.title("Получение списка фильмов")
def test_get_movies(unauthorized_api):

    res = unauthorized_api.movies_api.get_movies()
    body = MoviesListResponseModel(**res.json())

    assert len(body.movies) >= 0
    assert body.count >= 0


@pytest.mark.movies
@allure.title("Фильтрация и пагинация фильмов")
def test_get_movies_with_filters(unauthorized_api):

    res = unauthorized_api.movies_api.get_movies(params={
        "page": 2,
        "pageSize": 5
    })

    body = MoviesListResponseModel(**res.json())

    assert body.page == 2
    assert body.pageSize == 5


@pytest.mark.movies
@pytest.mark.negative
@allure.title("Неверный фильтр цены (minPrice > maxPrice)")
def test_invalid_price_filter(unauthorized_api):

    res = unauthorized_api.movies_api.get_movies(
        params={"minPrice": 500, "maxPrice": 100},
        expected_status=400
    )

    assert res.status_code == 400

@pytest.mark.movies
@pytest.mark.parametrize(
    "min_price,max_price,expected_status",
    [
        (1, 1000, 200),
        (100, 500, 200),
        (500, 100, 400),
    ]
)

# тест с параметризацией
@allure.title("GET /movies - проверка фильтра цены (parametrized)")
def test_movies_price_filter(unauthorized_api, min_price, max_price, expected_status):

    res = unauthorized_api.movies_api.get_movies(params={
        "minPrice": min_price,
        "maxPrice": max_price
    }, expected_status=expected_status)

    assert res.status_code == expected_status