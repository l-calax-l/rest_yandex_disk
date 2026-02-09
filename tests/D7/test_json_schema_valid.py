import allure

from helpers.allure_helpers import attach_api_response
from helpers.json_schema_validator import validate_schema


@allure.epic("Yandex Disk API")
@allure.feature("Валидация API (JSON Schema)")
@allure.story("Получение метаинформации о ресурсах")
@allure.title("TC-D7-01: Проверка схемы ответа GET /resources")
@allure.description(
    "Валидация структуры JSON-ответа при запросе информации о папке "
    "с вложенными файлами. Проверка обязательных полей и типов данных."
)
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("contract", "schema", "validation")
def test_d7_get_resources_schema(yandex_client, folder_factory):

    with allure.step("Предусловие: Создаем папку с файлом, чтобы ответ не был пустым"):
        folder_path = folder_factory("schema_test")
        file_content = b"test content"
        disk_path = f"{folder_path}/test_file.txt"

        upload_response = yandex_client.upload_resource(disk_path, file_content)
        attach_api_response(upload_response, 201)

    with allure.step("Получить информацию о папке (список файлов)"):
        response = yandex_client.get_folder_info(folder_path)
        attach_api_response(response, 200)
        assert (
            response.status_code == 200
        ), f"Ожидался статус 200, получен {response.status_code}"

    with allure.step(
        "Валидация схемы: проверяем, что ответ соответствует resources_schema.json"
    ):
        validate_schema(response.json(), "resources_schema.json")
