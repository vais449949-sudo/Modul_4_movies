import pytest
import allure
from data_generator.data_generator import DataGenerator


@pytest.mark.movies
@pytest.mark.slow
@pytest.mark.negative
@allure.title("Запрет создания фильма обычным пользователем")
def test_user_cannot_create_movie(common_user):

    movie_data = DataGenerator.movie()

    with allure.step("Попытка создать фильм обычным пользователем"):
        response = common_user.api.movies_api.create_movie(movie_data)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 403