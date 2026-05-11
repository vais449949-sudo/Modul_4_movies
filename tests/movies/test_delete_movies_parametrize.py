import pytest
import allure


@pytest.mark.movies
@pytest.mark.rbac
@pytest.mark.parametrize("user_fixture,expected_status", [
    ("super_admin", 200),
    ("admin_user", 403),
    ("common_user", 403),
])
@allure.title("Проверка прав на удаление фильма")
def test_delete_movie_rbac(
        request,
        created_movie,
        user_fixture,
        expected_status
):

    user = request.getfixturevalue(user_fixture)

    user.api.movies_api.delete_movie(
        created_movie["id"],
        expected_status=expected_status
    )

    if expected_status == 200:

        user.api.movies_api.get_movie(
            created_movie["id"],
            expected_status=404
        )