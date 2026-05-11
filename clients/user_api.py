from custom_requester.custom_requester import CustomRequester
from models.base_models import TestUser, RegisterUserResponse


class UserApi:
    """
    API для работы с пользователями.
    """

    def __init__(self, requester: CustomRequester):
        self.requester = requester

    def get_user(self, user_locator: str, expected_status: int = 200):
        return self.requester.send_request(
            method="GET",
            endpoint=f"user/{user_locator}",
            expected_status=expected_status
        )

    def create_user(self, data: TestUser, expected_status: int = 201):
        response = self.requester.send_request(
            method="POST",
            endpoint="user",
            data=data,
            expected_status=expected_status
        )

        return response