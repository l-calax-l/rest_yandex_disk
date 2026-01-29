import allure

from api.yandex_client import YandexDiskClient
from config import settings
from helpers.allure_helpers import attach_api_response, attach_validation_result


@allure.epic("Yandex Disk API")
@allure.feature("Получение информации о диске")
@allure.story("Успешное получение данных")
@allure.title("ТС-01 Авторизация с валидным токеном")
@allure.description("Проверка получения данных авторизированного пользователя")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("smoke", "auth", "positive")
def test_tc1_auth_valid_token(yandex_client):

    with allure.step("Отправить GET запрос по адресу v1/disk/"):
        response = yandex_client.get_disk_info()
        attach_api_response(response, expected_status=200)

    with allure.step("Проверить тело ответа и данные пользователя"):
        assert (
            response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

        user = response.json()["user"]

        attach_validation_result("Login", settings.yandex_login, user["login"])
        assert (
            user["login"] == settings.yandex_login
        ), f"Login ожидался '{settings.yandex_login}'"

        attach_validation_result(
            "Display Name", settings.yandex_display_name, user["display_name"]
        )
        assert (
            user["display_name"] == settings.yandex_display_name
        ), f"Name ожидался '{settings.yandex_display_name}'"


@allure.epic("Yandex Disk API")
@allure.feature("Получение информации о диске")
@allure.story("Обработка ошибок доступа")
@allure.title("ТС-02 Авторизация без токена")
@allure.description(
    "Проверка получения 401 ошибки при запросе без заголовка Authorization"
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("security", "auth", "negative")
def test_tc2_auth_missing_token():
    no_auth_client = YandexDiskClient(token=None)

    with allure.step("Отправить GET запрос по адресу v1/disk/ без передачи токена"):
        response = no_auth_client.get_disk_info()
        attach_api_response(response, expected_status=401)

    with allure.step("Проверить статус код и структуру ошибки"):
        assert (
            response.status_code == 401
        ), f"Ожидался 401, получен {response.status_code}"

        result = response.json()

        attach_validation_result("Error", "UnauthorizedError", result.get("error"))
        assert (
            result["error"] == "UnauthorizedError"
        ), f"Ожидался 'UnauthorizedError', получен {result['error']} "
        assert "description" in result, "В ответе нет поля 'description'"
        assert "message" in result, "В ответе нет поля 'message'"
