import pytest
import allure
import pytest_check as check


class TestUser:

    @allure.title("Создание пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, super_admin, creation_user_data):

        with allure.step("Создаём пользователя через API"):
            response = super_admin.api.user_api.create_user(
                creation_user_data
            ).json()

        with allure.step("Проверяем поля ответа пользователя"):
            with allure.step("Проверка ID"):
                check.is_true(response.get('id'), "ID должен быть не пустым")

            with allure.step("Проверка email"):
                check.equal(response.get('email'), creation_user_data.email)

            with allure.step("Проверка fullName"):
                check.equal(response.get('fullName'), creation_user_data.fullName)

            with allure.step("Проверка roles"):
                check.is_in("USER", response.get('roles', []))

            with allure.step("Проверка verified"):
                check.is_true(response.get('verified'))

            with allure.step("Проверка banned"):
                check.is_false(response.get('banned'))


    @allure.title("Получение пользователя по ID и email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_locator(self, super_admin, creation_user_data):

        with allure.step("Создаём пользователя"):
            created_user_response = super_admin.api.user_api.create_user(
                creation_user_data
            ).json()

        with allure.step("Получаем пользователя по ID"):
            response_by_id = super_admin.api.user_api.get_user(
                created_user_response['id']
            ).json()

        with allure.step("Получаем пользователя по email"):
            response_by_email = super_admin.api.user_api.get_user(
                creation_user_data.email
            ).json()

        with allure.step("Сравниваем ответы"):
            check.equal(response_by_id, response_by_email)

        with allure.step("Проверка полей ответа"):
            check.is_true(response_by_id.get('id'))
            check.equal(response_by_id.get('email'), creation_user_data.email)
            check.equal(response_by_id.get('fullName'), creation_user_data.fullName)
            check.is_in("USER", response_by_id.get('roles', []))
            check.is_true(response_by_id.get('verified'))


    @pytest.mark.slow
    @allure.title("Запрет доступа обычному пользователю")
    def test_common_user_cannot_get_user_by_id(self, common_user):

        with allure.step("Попытка получить пользователя без прав"):
            response = common_user.api.user_api.get_user(
                common_user.email,
                expected_status=403
            )