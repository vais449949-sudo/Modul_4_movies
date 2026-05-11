from clients.auth_api import AuthAPI
from clients.movies_api import MoviesAPI
from clients.user_api import UserApi
from clients.genres_api import GenresAPI

class ApiManager:
    """
    Центральный менеджер API.
    Отвечает за:
    - инициализацию API клиентов
    - авторизацию
    - управление токеном
    """

    def __init__(self, auth_requester, movies_requester):
        self.auth_requester = auth_requester
        self.movies_requester = movies_requester

        self.auth_api = AuthAPI(auth_requester)
        self.movies_api = MoviesAPI(movies_requester)
        self.user_api = UserApi(auth_requester)
        self.genres_api = GenresAPI(movies_requester)

        self.token = None

    def authenticate(self, email: str, password: str):
        """
        Авторизация пользователя.
        Получение и установка Bearer token во все requesters.
        """

        response = self.auth_api.login_user({
            "email": email,
            "password": password
        })

        token = response.json().get("accessToken")

        if not token:
            raise AssertionError("Token not found in response")

        self.token = token

        auth_header = {"Authorization": f"Bearer {token}"}

        self.auth_requester._update_session_headers(**auth_header)
        self.movies_requester._update_session_headers(**auth_header)

    def close_session(self):
        """Закрытие HTTP сессий"""
        self.auth_requester.session.close()
        self.movies_requester.session.close()
