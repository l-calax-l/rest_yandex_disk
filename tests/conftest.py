import allure
import pytest
from faker import Faker

from api.clients.yandex_client import YandexDiskClient
from config import settings

fake = Faker()


@pytest.fixture
def yandex_client():
    assert settings.yandex_token, "Ошибка: Не задан YANDEX_TOKEN в настройках"

    client = YandexDiskClient(token=settings.yandex_token)
    yield client
    client.session.close()


@pytest.fixture
def yandex_no_auth_client():
    assert settings.yandex_token, "Ошибка: Не задан YANDEX_TOKEN в настройках"

    client = YandexDiskClient(token=None)
    yield client
    client.session.close()


@pytest.fixture(scope="function")
def new_resource_cleanup(yandex_client):

    created_resources = []
    yield created_resources
    if created_resources:
        with allure.step(f"Cleanup: Удаление {len(created_resources)} ресурсов"):
            for resource in created_resources:
                yandex_client.delete_resource(resource, permanently=True)


@pytest.fixture(scope="function")
def folder_factory(yandex_client):
    created_folders = []

    def _create_folder(folder_name=None):

        if not folder_name:
            folder_name = f"TestFolder_{fake.uuid4()}"

        yandex_client.create_folder(folder_name)

        created_folders.append(folder_name)

        return folder_name

    yield _create_folder

    for folder_name in created_folders:
        yandex_client.delete_resource(folder_name, permanently=True)
