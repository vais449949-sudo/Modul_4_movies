import requests
import json
import logging


class CustomRequester:
    """
    Универсальная обертка над requests.
    Отвечает за:
    - отправку HTTP-запросов
    - проверку статус-кодов
    - логирование
    """

    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()

        # базовый логгер
        self.logger = logging.getLogger(__name__)
#        self.logger.setLevel(logging.INFO)

    def send_request(
            self,
            method: str,
            endpoint: str,
            data: dict = None,
            params: dict = None,
            headers: dict = None,
            expected_status: int = 200,
            need_logging: bool = True
    ):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=final_headers,
            timeout=10
        )

        if need_logging:
            self._log_request_and_response(response)

        if expected_status is not None and response.status_code != expected_status:
            raise AssertionError(
                f"\n Unexpected status code\n"
                f"Expected: {expected_status}\n"
                f"Actual: {response.status_code}\n"
                f"URL: {url}\n"
                f"Response: {response.text}"
            )

        return response

    def _update_session_headers(self, **kwargs):
        """
        Обновление заголовков (например Authorization)
        """
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def _log_request_and_response(self, response):
        """
        Красивое логирование запроса в стиле curl + ответ
        """
        try:
            request = response.request

            # --- REQUEST ---
            headers = " \\\n".join(
                [f"-H '{k}: {v}'" for k, v in request.headers.items()]
            )

            body = ""
            if request.body:
                if isinstance(request.body, bytes):
                    body = request.body.decode("utf-8")
                if body != "{}":
                    body = f"-d '{body}'"

            self.logger.info("\n" + "=" * 40 + " REQUEST " + "=" * 40)
            self.logger.info(
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            # --- RESPONSE ---
            try:
                response_data = json.dumps(
                    response.json(),
                    indent=4,
                    ensure_ascii=False
                )
            except Exception:
                response_data = response.text

            self.logger.info("\n" + "=" * 40 + " RESPONSE " + "=" * 40)
            self.logger.info(f"STATUS: {response.status_code}")
            self.logger.info(f"BODY:\n{response_data}")
            self.logger.info("=" * 90 + "\n")

        except Exception as e:
            self.logger.error(f"Logging error: {e}")