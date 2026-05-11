from constants import GENRES_ENDPOINT


class GenresAPI:
    """
    API-класс для работы с жанрами.
    """

    def __init__(self, requester):
        self.requester = requester

    def get_genres(self, expected_status: int = 200):
        """
        Получение списка жанров.

        :param expected_status: ожидаемый статус ответа
        :return: ответ API
        """
        return self.requester.send_request(
            method="GET",
            endpoint=GENRES_ENDPOINT,
            expected_status=expected_status
        )