from constants import MOVIES_ENDPOINT
from models.movie_response_model import MovieResponseModel

class MoviesAPI:
    """
    API-класс для работы с фильмами.
    """

    def __init__(self, requester):
        self.requester = requester

    # -------- GET /movies -------- #
    def get_movies(self, params: dict = None, expected_status: int = 200):
        """
        Получение списка фильмов с возможными фильтрами.

        :param params: Параметры запроса (пагинация, фильтры)
        :param expected_status: Ожидаемый статус-код
        :return: Ответ API
        """
        return self.requester.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    # -------- GET /movies/{id} -------- #
    def get_movie(self, movie_id: int, expected_status: int = 200):
        return self.requester.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    # -------- POST /movies -------- #
    def create_movie(self, payload: dict, expected_status: int = None):
        """
        Создание нового фильма.

        :param payload: Данные для создания фильма
        :param expected_status: Ожидаемый статус-код
        :return: Ответ API
        """
        return self.requester.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=payload,
            expected_status=expected_status
        )

    # -------- PATCH /movies/{id} -------- #
    def update_movie(self, movie_id: int, payload: dict, expected_status: int = 200):
        return self.requester.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=payload,
            expected_status=expected_status
        )

    # -------- DELETE /movies/{id} -------- #
    def delete_movie(self, movie_id: int, expected_status: int = 200):
        """
        Удаление фильма по ID.

        :param movie_id: ID фильма
        :param expected_status: Ожидаемый статус-код
        :return: Ответ API
        """
        return self.requester.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
    #ментод для теста по обновлению фильма
    def get_movie_model(self, movie_id: int, expected_status: int = 200):
        response = self.requester.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

        return self.requester.parse_json(response, MovieResponseModel)
    #метод для теста по обновлению фильма
    def update_movie_model(self, movie_id: int, payload: dict, expected_status: int = 200):
        response = self.requester.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=payload,
            expected_status=expected_status
        )

        return self.requester.parse_json(response, MovieResponseModel)