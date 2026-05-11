from clients.api_manager import ApiManager


class User:
    """
    Тестовая сущность пользователя для работы в API тестах.
    Хранит данные пользователя и ссылку на API клиент.
    """

    def __init__(self, email: str, password: str, roles: list[str], api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        """
        Возвращает учетные данные пользователя (email, password)
        """
        return self.email, self.password