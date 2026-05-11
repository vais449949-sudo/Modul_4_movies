import requests
import json
import logging
import os

from pydantic import BaseModel
from constants import RED, GREEN, RESET


class CustomRequester:
    """
    Универсальная обертка над requests.
    Отвечает за:
    - отправку HTTP запросов
    - логирование (curl формат)
    - проверку статус-кодов
    - поддержку Pydantic моделей
    """

    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.session.headers = self.base_headers.copy()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
        self,
        method: str,
        endpoint: str,
        data=None,
        params=None,
        headers: dict = None,
        expected_status: int = 200,
        need_logging: bool = True
    ):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        final_headers = self.session.headers.copy()
        if headers:
            final_headers.update(headers)

        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_none=True, exclude_unset=True)

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=final_headers,
            timeout=10
        )

        if need_logging:
            self.log_request_and_response(response)

        if expected_status is not None and response.status_code != expected_status:
            raise AssertionError(
                f"\nExpected: {expected_status}\n"
                f"Actual: {response.status_code}\n"
                f"URL: {url}\n"
                f"Response: {response.text}"
            )

        return response

    def set_auth_headers(self, **kwargs):
        """Установка auth headers (Bearer token и т.д.)"""
        self.session.headers.update(kwargs)

    def _update_session_headers(self, **kwargs):
        """Старый метод для обновления headers (используется в ApiManager/AuthAPI)"""
        self.session.headers.update(kwargs)

    def log_request_and_response(self, response):
        try:
            request = response.request

            headers = " \\\n".join(
                [f"-H '{h}: {v}'" for h, v in request.headers.items()]
            )

            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '')}"

            body = ""
            if request.body:
                body = request.body.decode() if isinstance(request.body, bytes) else request.body
                body = f"-d '{body}' \n" if body != '{}' else ""

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            if not response.ok:
                self.logger.info(
                    f"\tRESPONSE:"
                    f"\nSTATUS_CODE: {RED}{response.status_code}{RESET}"
                    f"\nDATA: {RED}{response.text}{RESET}"
                )

        except Exception as e:
            self.logger.info(f"\nLogging error: {type(e)} - {e}")