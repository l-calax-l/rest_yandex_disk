import logging

import requests

from api.base_client import BaseClient
from api.endpoints import YandexDiskEndpoints
from api.models.yandex_models import CopyResourceRequest, LinkRequest, LinkResponse

logger = logging.getLogger(__name__)


class YandexDiskClient(BaseClient):

    def get_disk_info(self):
        """Информация о диске"""
        return self.get(YandexDiskEndpoints.DISK)

    def create_folder(self, folder_path: str) -> requests.Response:
        """Создание папки"""
        return self.put(YandexDiskEndpoints.RESOURCES, params={"path": folder_path})

    def get_folder_info(self, folder_path: str) -> requests.Response:
        """Информация о папке"""
        return self.get(YandexDiskEndpoints.RESOURCES, params={"path": folder_path})

    def get_trash_resource_info(self, path: str):
        """Информация о файлах в корзине"""
        return self.get(YandexDiskEndpoints.TRASH, params={"path": path})

    def get_trash_path_by_name(self, name: str) -> str | None:
        """
        Делает 1 запрос к корзине.
        Возвращает путь (str), если нашел.
        Возвращает None, если не нашел.
        """
        response = self.get(YandexDiskEndpoints.TRASH, params={"limit": 50})

        if response.status_code == 200:
            items = response.json().get("_embedded", {}).get("items", [])
            for item in items:
                if item.get("name") == name:
                    return item.get("path")

        return None

    def restore_resource(self, path: str):
        """Восстановление ресурса из корзины"""
        return self.put(YandexDiskEndpoints.TRASH_RESTORE, params={"path": path})

    def delete_resource(
        self, folder_path: str, permanently: bool = False
    ) -> requests.Response:
        """
        Удаляет ресурс.
        folder_path: путь папка/файл;
        permanently: True = удалить навсегда, False = в корзину.
        """
        return self.delete(
            YandexDiskEndpoints.RESOURCES,
            params={"path": folder_path, "permanently": str(permanently).lower()},
        )

    def upload_resource(
        self, file_path: str, content: str | bytes
    ) -> requests.Response:
        """Загрузка файла с заполнением данных GET + PUT"""

        request_model = LinkRequest(path=file_path, overwrite=True)

        link_response = self.get(
            YandexDiskEndpoints.RESOURCES_UPLOAD, params=request_model.model_dump()
        )

        href = LinkResponse(**link_response.json()).href
        return requests.put(href, data=content)

    def copy_resource(self, from_path: str, to_path: str) -> requests.Response:
        """Копирование ресурса from - откуда / path - куда"""
        request_model = CopyResourceRequest(
            from_path=from_path, path=to_path, overwrite=False
        )
        params = request_model.model_dump()
        params["from"] = params.pop("from_path")

        return self.post(YandexDiskEndpoints.RESOURCES_COPY, params=params)

    def get_download_link(self, file_path: str) -> requests.Response:
        """Получение ссылки на ресурс"""
        request_model = LinkRequest(path=file_path)
        return self.get(
            YandexDiskEndpoints.RESOURCES_DOWNLOAD, params=request_model.model_dump()
        )

    def download_file(self, url: str) -> bytes:
        """Получение контента по ссылке"""
        return requests.get(url).content
