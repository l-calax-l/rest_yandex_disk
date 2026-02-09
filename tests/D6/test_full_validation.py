import allure

from api.models.yandex_models import ErrorResponse, LinkResponse
from helpers.allure_helpers import attach_api_response, attach_validation_result


@allure.epic("Yandex Disk API")
@allure.feature("Операции с файлами")
@allure.story("Загрузка и копирование")
@allure.title("TC-D6-03: Загрузка и копирование файла с полной валидацией")
@allure.description(
    "Проверка полного цикла: загрузка файла, успешное копирование (201), "
    "повторное копирование с конфликтом (409). Валидация JSON через Data-классы."
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "negative", "files", "copy", "validation")
def test_tc03_upload_and_copy(yandex_client, folder_factory):

    with allure.step("Предусловия: создать папки input_data и output_data"):
        input_folder = folder_factory("input_data")
        output_folder = folder_factory("output_data")

    file_name = "data.txt"
    file_content = b"username=SDET\npassword=secret_key"
    disk_path = f"{input_folder}/{file_name}"
    copy_path = f"{output_folder}/{file_name}"

    with allure.step(f"Загрузка сгенерированного текстового файла в {disk_path}"):
        upload_response = yandex_client.upload_resource(disk_path, file_content)
        attach_api_response(upload_response, 201)
        assert (
            upload_response.status_code == 201
        ), f"Ожидался статус 201, получен: {upload_response.status_code}"

    with allure.step("Копирование файла (1-й раз)"):
        copy_response = yandex_client.copy_resource(disk_path, copy_path)
        attach_api_response(copy_response, 201)
        assert (
            copy_response.status_code == 201
        ), f"Ожидался статус 201, получен: {copy_response.status_code}"

        copy_data = LinkResponse(**copy_response.json())
        assert (
            copy_data.method == "GET"
        ), f"В ответе ожидался method: GET, получен: {copy_data.method}"

    with allure.step("Попытка повторного копирования файла"):
        conflict_response = yandex_client.copy_resource(disk_path, copy_path)
        attach_api_response(conflict_response, 409)
        assert (
            conflict_response.status_code == 409
        ), f"Ожидался статус 409, получен: {conflict_response}"

        error_data = ErrorResponse(**conflict_response.json())
        expected_error = "DiskResourceAlreadyExistsError"
        assert (
            error_data.error == expected_error
        ), f"Ожидалась ошибка {expected_error},получен {error_data.error} "
        assert error_data.message, "В ответе отсутствует поле message"
        assert error_data.description, "В ответе отсутствует поле description"


@allure.epic("Yandex Disk API")
@allure.feature("Операции с файлами")
@allure.story("Скачивание файлов")
@allure.title("TC-D6-04: Скачивание файла и проверка контента")
@allure.description(
    "Проверка получения ссылки на скачивание, загрузка файла по ссылке "
    "и побитовое сравнение содержимого с оригиналом."
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "files", "download", "validation")
def test_tc04_download_file(yandex_client, folder_factory):

    with allure.step(
        f"Предусловие: генерация текстового файла 'data.txt' и загрузка файла в папку 'sdet_data' "
    ):
        sdet_folder = folder_factory("sdet_data")

        file_name = "data.txt"
        original_content = b"username=SDET\npassword=secret_key"
        disk_path = f"{sdet_folder}/{file_name}"

        upload_resp = yandex_client.upload_resource(disk_path, original_content)
        attach_api_response(upload_resp, 201)
        assert (
            upload_resp.status_code == 201
        ), f"Ожидался статус 201, получен: {upload_resp.status_code}"

    with allure.step("Получить ссылку на скачивание"):
        response = yandex_client.get_download_link(disk_path)
        attach_api_response(response, 200)
        assert (
            response.status_code == 200
        ), f"Ожидался статус 200, получен: {response.status_code}"

        download_link = LinkResponse(**response.json())
        assert "http" in download_link.href, "В ответе отсутствует путь http"
        assert (
            download_link.method == "GET"
        ), f"В ответе ожидался method: GET, получен: {download_link.method}"

    with allure.step("Скачать файл и сравнить контент"):
        downloaded_content = yandex_client.download_file(download_link.href)
        attach_validation_result("Content", original_content, downloaded_content)
        assert (
            downloaded_content == original_content
        ), f"Контент не совпадает! Ожидалось: {original_content}, Получено: {downloaded_content}"
