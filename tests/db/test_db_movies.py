import pytest
import allure
from data_generator.data_generator import DataGenerator


@pytest.mark.movies
@pytest.mark.db
@allure.title("CRUD фильма с проверкой в БД")
def test_movie_crud_db(super_admin, db_helper):

    # Подготовка тестовых данных
    movie_data = DataGenerator.movie()
    movie_data.pop("id", None)  # ID создаётся на стороне API

    # Создание фильма через API
    created_movie = super_admin.api.movies_api.create_movie(movie_data).json()
    movie_id = created_movie["id"]

    # Проверка: фильм сохранён в БД
    db_movie = db_helper.get_movie_by_id(movie_id)

    assert db_movie is not None
    assert db_movie.id == movie_id
    assert db_movie.name == movie_data["name"]

    # Удаление фильма через API
    super_admin.api.movies_api.delete_movie(movie_id)

    # Проверка: фильм удалён из БД
    assert db_helper.get_movie_by_id(movie_id) is None