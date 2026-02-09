import pytest

from api.yandex_client import YandexDiskClient
from config import settings


@pytest.fixture
def yandex_client():
    assert settings.yandex_token, "Ошибка: Не задан YANDEX_TOKEN в настройках"

    client = YandexDiskClient(token=settings.yandex_token)
    yield client
    client.session.close()
