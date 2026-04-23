from clients.auth_api import AuthAPI
from clients.movies_api import MoviesAPI

class ApiManager:
    """
    Api манагер для авторизации и работы с фильмами.
    """

    def __init__(self, auth_requester, movies_requester):
        self.auth_api = AuthAPI(auth_requester)
        self.movies_api = MoviesAPI(movies_requester)

        self.auth_requester = auth_requester
        self.movies_requester = movies_requester

    def authenticate(self, email: str, password: str):
        """
        Авторизация пользователя и обновление токена для всех API
        """
        response = self.auth_api.login_user({
            "email": email,
            "password": password
        })

        token = response.json().get("accessToken")
        if not token:
            raise AssertionError("Token not found in response")

        auth_header = {"Authorization": f"Bearer {token}"}

        # Обновляем заголовки как для auth_requester, так и для movies_requester
        self.auth_requester._update_session_headers(**auth_header)
        self.movies_requester._update_session_headers(**auth_header)

