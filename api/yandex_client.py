import logging

import allure
import requests

from config import settings

logger = logging.getLogger(__name__)


class YandexDiskClient:
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

    @allure.step("Получить информацию о диске")
    def get_disk_info(self):
        return self._send_request("GET", "/v1/disk/")
