import pytest
import allure


@pytest.mark.movies
@pytest.mark.parametrize("page,page_size", [
    (1, 5),
    (2, 5),
    (3, 10),
])
@allure.title("Проверка пагинации фильмов")
def test_get_movies_with_filters(unauthorized_api, page, page_size):

    res = unauthorized_api.movies_api.get_movies(params={
        "page": page,
        "pageSize": page_size
    })

    body = res.json()

    assert body["page"] == page
    assert body["pageSize"] == page_size


@pytest.mark.movies
@pytest.mark.negative
@pytest.mark.parametrize("min_price,max_price", [
    (500, 100),
    (-10, 100),
    (100, -50),
    ("abc", 100),
])
@allure.title("Невалидные фильтры цены")
def test_invalid_price_filter(unauthorized_api, min_price, max_price):

    res = unauthorized_api.movies_api.get_movies(
        params={"minPrice": min_price, "maxPrice": max_price},
        expected_status=400
    )

    assert res.status_code == 400