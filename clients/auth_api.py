from constants import LOGIN_ENDPOINT
from models.base_models import LoginRequest, LoginResponse


class AuthAPI:
    """
    API-класс для работы с авторизацией.
    """

    def __init__(self, requester):
        self.requester = requester

    def login_user(self, data: LoginRequest, expected_status: int = 200):
        """
        Логин пользователя.
        """
        return self.requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=data.model_dump(),
            expected_status=expected_status
        )

    def authenticate(self, email: str, password: str):
        """
        Авторизация и установка токена в headers.
        """
        login_data = LoginRequest(email=email, password=password)

        response = self.login_user(login_data).json()

        token = LoginResponse.model_validate(response).accessToken

        self.requester._update_session_headers(
            Authorization=f"Bearer {token}"
        )