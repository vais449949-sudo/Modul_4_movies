import pytest
import allure
from uuid import uuid4


@pytest.mark.movies
@pytest.mark.regression
@allure.title("Обновление фильма (PATCH /movies/{id} + DB проверка)")
def test_patch_movie(super_admin, db_helper):

    movies_api = super_admin.api.movies_api

    # 1. CREATE (API)
    base_payload = {
        "name": f"Movie {uuid4()}",
        "price": 100,
        "description": "Test",
        "location": "MSK",
        "published": True,
        "genreId": 1
    }

    created = movies_api.create_movie(base_payload)
    movie_id = created.json()["id"]

    # 2. CHECK CREATE (DB)
    db_helper.db_session.expire_all()
    db_movie = db_helper.get_movie_by_id(movie_id)

    assert db_movie is not None
    assert db_movie.name == base_payload["name"]
    assert db_movie.price == base_payload["price"]

    # 3. UPDATE (API)
    patch_payload = {
        "name": f"UPDATED {uuid4()}",
        "price": 200,
        "description": "Updated",
        "location": "MSK",
        "published": True,
        "genreId": 1
    }

    updated = movies_api.update_movie(movie_id, patch_payload)

    # 4. CHECK UPDATE (DB)
    db_helper.db_session.expire_all()
    updated_db_movie = db_helper.get_movie_by_id(movie_id)

    assert updated_db_movie is not None
    assert updated_db_movie.name == patch_payload["name"]
    assert updated_db_movie.price == patch_payload["price"]
    assert updated_db_movie.description == patch_payload["description"]
    assert updated_db_movie.location == patch_payload["location"]
    assert updated_db_movie.published == patch_payload["published"]

    # 5. OPTIONAL: API check
    fetched = movies_api.get_movie_model(movie_id)

    assert fetched.name == patch_payload["name"]
    assert fetched.price == patch_payload["price"]


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

