import requests



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