import pytest
import requests
import uuid

from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager
from constants import AUTH_BASE_URL, MOVIES_BASE_URL
from data_generator.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants import Roles
from models.base_models import TestUser
from db_requester.db_helpers import DBHelper
from db_requester.db_client import SessionLocal


# =========================================================
# ОБЩИЙ ФАБРИЧНЫЙ МЕТОД ДЛЯ API
# =========================================================

def create_api():
    session = requests.Session()

    auth_requester = CustomRequester(session, AUTH_BASE_URL)
    movies_requester = CustomRequester(session, MOVIES_BASE_URL)

    return ApiManager(auth_requester, movies_requester)


# =========================================================
# FIXTURES API
# =========================================================

@pytest.fixture
def api_manager():
    return create_api()


@pytest.fixture
def unauthorized_api():
    return create_api()


@pytest.fixture
def user_session():
    def _create():
        return create_api()
    return _create


# =========================================================
# MOVIES FIXTURES
# =========================================================

@pytest.fixture
def created_movie(super_admin):
    movie_data = DataGenerator.movie()
    movie_data.pop("id", None)

    genres = super_admin.api.genres_api.get_genres().json()
    movie_data["genreId"] = genres[0]["id"]

    response = super_admin.api.movies_api.create_movie(movie_data)
    assert response.status_code in (200, 201), response.text

    return response.json()


# =========================================================
# USERS FIXTURES
# =========================================================

@pytest.fixture
def super_admin(user_session, db_helper):
    api = user_session()

    user = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        api
    )

    # DB helper (лучше было бы через сервис слой, но оставим как есть)
    user.db_helper = db_helper

    user.api.auth_api.authenticate(
        user.creds[0],
        user.creds[1]
    )

    return user


@pytest.fixture
def test_user():
    password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=password,
        passwordRepeat=password,
        roles=[Roles.USER.value],
        verified=False,
        banned=False
    )


@pytest.fixture
def creation_user_data(test_user: TestUser):
    updated = test_user.model_copy()
    updated.fullName = f"Tester {uuid.uuid4().hex[:6]}"
    return updated


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    api = user_session()

    response = super_admin.api.user_api.create_user(
        creation_user_data
    ).json()

    user = User(
        email=response["email"],
        password=creation_user_data.password,
        roles=response["roles"],
        api=api
    )

    user.api.auth_api.authenticate(
        user.email,
        creation_user_data.password
    )

    return user


@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    api = user_session()

    data = creation_user_data.model_copy()
    data.fullName = f"Admin {uuid.uuid4().hex[:6]}"
    data.roles = [Roles.ADMIN.value]
    data.email = DataGenerator.generate_random_email()

    response = super_admin.api.user_api.create_user(data).json()

    user = User(
        email=response["email"],
        password=data.password,
        roles=response["roles"],
        api=api
    )

    user.api.auth_api.authenticate(
        user.email,
        data.password
    )

    return user


# =========================================================
# DB FIXTURES
# =========================================================

@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def db_helper(db_session):
    return DBHelper(db_session)


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user

    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)