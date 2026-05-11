from enum import Enum

AUTH_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru" # URL для авторизации (получение токена)
MOVIES_BASE_URL = "https://api.dev-cinescope.coconutqa.ru"  # URL для работы с фильмами

LOGIN_ENDPOINT = "/login" # Эндпоинт аутентификации пользователя
MOVIES_ENDPOINT = "/movies" # Эндпоинт для работы с фильмами
GENRES_ENDPOINT = "/genres" # Эндпоинт для работы с жанрами фильмов


RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
