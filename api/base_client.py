import logging

import allure
import requests

from config import settings

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, token):
        self.base_url = settings.base_url
        self.session = requests.Session()

        if token:
            self.session.headers.update({"Authorization": "OAuth " + token})

    def _send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Request: {method} {url}")

        with allure.step(f"{method} {endpoint}"):
            response = self.session.request(method, url, **kwargs)

            return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request("DELETE", endpoint, **kwargs)
