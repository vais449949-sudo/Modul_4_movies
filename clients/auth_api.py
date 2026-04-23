from constants import LOGIN_ENDPOINT


class AuthAPI:
    """
    API-класс для работы с авторизацией.
    """

    def __init__(self, requester):
        self.requester = requester

    def login_user(self, credentials: dict, expected_status: int = 200):
        """
        Логин пользователя.

        :param credentials: {"email": str, "password": str}
        :param expected_status: ожидаемый статус-код
        """
        return self.requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=credentials,
            expected_status=expected_status
        )

    def authenticate(self, creds: tuple):
        """
        Авторизация и установка токена в headers.

        :param creds: (email, password)
        """
        email, password = creds

        response = self.login_user({
            "email": email,
            "password": password
        }).json()

        token = response.get("accessToken")
        if not token:
            raise AssertionError(" accessToken отсутствует в ответе")

        self.requester._update_session_headers(
            Authorization=f"Bearer {token}"
        )