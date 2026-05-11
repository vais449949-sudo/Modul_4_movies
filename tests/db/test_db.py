import pytest
import allure


@pytest.mark.movies
@pytest.mark.db
@allure.title("Проверка данных пользователя в БД")
def test_db_requests(super_admin, db_helper, created_test_user):

    with allure.step("Проверяем пользователя по ID в БД"):
        db_user = db_helper.get_user_by_id(created_test_user.id)
        assert db_user is not None
        assert db_user.id == created_test_user.id

    with allure.step("Проверяем пользователя по email из фикстуры"):
        assert db_helper.user_exists_by_email(created_test_user.email)