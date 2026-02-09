import allure
from faker import Faker

from helpers.allure_helpers import attach_api_response, attach_validation_result
from helpers.wait import wait_for_result

fake = Faker()


@allure.epic("Yandex Disk API")
@allure.feature("Управление папками")
@allure.story("Создание ресурсов")
@allure.title("TC-D4-01: Создание новой папки")
@allure.description(
    "Проверка создания папки методом PUT и валидация созданного ресурса"
)
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("positive", "resources", "create")
def test_tc1_create_folder(yandex_client, new_resource_cleanup):

    folder_name = f"TestFolder_{fake.uuid4()}"

    with allure.step(f"Отправить PUT запрос на создание папки  {folder_name}"):
        create_response = yandex_client.create_folder(folder_name)
        attach_api_response(create_response, expected_status=201)

    new_resource_cleanup.append(folder_name)

    with allure.step("Проверить тело ответа и данные"):
        data = create_response.json()
        attach_validation_result("href", folder_name, data.get("href"))

        assert (
            create_response.status_code == 201
        ), f"Папка не создалась, получен {create_response.status_code}"
        assert "href" in data, "В ответе отсутствует поле href"

    with allure.step(f"Отправить GET запрос на получение папки {folder_name}"):
        get_response = yandex_client.get_folder_info(folder_name)
        attach_api_response(get_response, expected_status=200)

        result = get_response.json()
        assert (
            result.get("type") == "dir"
        ), f"В ответе некорректный type:{result.get('type')}"
        assert folder_name in get_response.json().get(
            "name"
        ), "В ответе некорректный имя"


@allure.epic("Yandex Disk API")
@allure.feature("Управление папками")
@allure.story("Удаление ресурсов")
@allure.title("TC-D4-02: Перманентное удаление папки")
@allure.description("Создание папки и её полное удаление (мимо корзины)")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "resources", "delete")
def test_tc2_delete_folder(yandex_client, folder_factory):
    folder_name = folder_factory()

    with allure.step("Предусловие: Убедится, что папка действительно существует"):
        response = yandex_client.get_folder_info(folder_name)
        attach_api_response(response, expected_status=200)
        assert (
            response.status_code == 200
        ), f"Ожидался статус 200,получен {response.status_code}"

    with allure.step(f"Отправить DELETE запрос на удаление папки {folder_name}"):
        delete_response = yandex_client.delete_resource(folder_name, permanently=True)
        expected_status_code = [202, 204]
        attach_api_response(delete_response, expected_status=expected_status_code)
        assert (
            delete_response.status_code in expected_status_code
        ), f"Ожидался один из {expected_status_code}, получен {delete_response.status_code}"

    with allure.step(f"Отправить GET запрос для удаленной папки {folder_name}"):
        get_response = yandex_client.get_folder_info(folder_name)
        attach_api_response(get_response, expected_status=404)
        assert (
            get_response.status_code == 404
        ), f"Ожидался статус 404, получен {get_response.status_code}"


@allure.epic("Yandex Disk API")
@allure.feature("Корзина и Восстановление")
@allure.story("Восстановление ресурсов")
@allure.title("TC-D4-03: Восстановление папки из корзины")
@allure.description("Удаление папки в корзину, поиск в корзине и восстановление")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "trash", "restore")
def test_tc3_delete_folder(yandex_client, folder_factory):
    folder_name = folder_factory()

    with allure.step("Удалить в корзину"):
        delete_response = yandex_client.delete_resource(folder_name, permanently=False)
        attach_api_response(delete_response, expected_status=[202, 204])
        assert delete_response.status_code in [202, 204]

    with allure.step(f"Найти путь к папке {folder_name[:10]} в корзине "):
        trash_path = wait_for_result(
            lambda: yandex_client.get_trash_path_by_name(folder_name),
            error_message=f"Не нашли папку {folder_name} в корзине",
        )
        attach_validation_result("Trash path", folder_name, trash_path)
        assert (
            folder_name in trash_path
        ), "Некорректный путь:название папки не совпадает с действительной  "

    with allure.step("Восстановить папку"):
        restore_response = yandex_client.restore_resource(trash_path)
        attach_api_response(restore_response, expected_status=[201, 202])
        assert restore_response.status_code in [201, 202]

    with allure.step("Проверить, что папка вернулась"):
        get_response = wait_for_result(
            lambda: yandex_client.get_folder_info(folder_name),
            error_message=f"Не нашли папку {folder_name} на диске",
        )

        attach_api_response(get_response, expected_status=200)
        assert get_response.status_code == 200


@allure.epic("Yandex Disk API")
@allure.feature("Управление папками")
@allure.story("Создание ресурсов")
@allure.title("TC-D4-04: Создание папки с уже существующим именем")
@allure.description("Проверка создания папки с уже существующим именем методом PUT")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("negative", "resources", "create")
def test_tc4_create_duplicate_folder(yandex_client, folder_factory):
    folder_name = folder_factory()

    with allure.step(f"Отправить PUT запрос на создание папки {folder_name}"):
        create_response = yandex_client.create_folder(folder_name)
        attach_api_response(create_response, expected_status=409)

    with allure.step("Проверить статус 409 и код ошибки"):
        assert (
            create_response.status_code == 409
        ), f"Ожидался статус 409, получен {create_response.status_code}"

        data = create_response.json()
        error_code = data.get("error")

        expected_error = "DiskPathPointsToExistentDirectoryError"
        attach_validation_result("Error Code", expected_error, error_code)

        assert (
            error_code == expected_error
        ), f"Неверный код ошибки. Ожидался '{expected_error}', получен '{error_code}'"


@allure.epic("Yandex Disk API")
@allure.feature("Управление папками")
@allure.story("Удаление ресурсов")
@allure.title("TC-D4-05: Удаление несуществующей папки")
@allure.description("Проверка удаления папки с несуществующим именем")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "resources", "delete")
def test_tc5_delete_folder_with_non_existent_name(yandex_client, folder_factory):
    fake_folder_name = f"TestFolder_{fake.uuid4()}"

    with allure.step("Предусловие: Убедится, что папка действительно не существует"):
        response = yandex_client.get_folder_info(fake_folder_name)
        attach_api_response(response, expected_status=404)
        assert (
            response.status_code == 404
        ), f"Ожидался статус 404,получен {response.status_code}"

    with allure.step(f"Отправить DELETE запрос на удаление папки {fake_folder_name}"):
        delete_response = yandex_client.delete_resource(
            fake_folder_name, permanently=True
        )
        data = delete_response.json()
        error_code = data.get("error")
        expected_error = "DiskNotFoundError"
        attach_api_response(delete_response, expected_status=404)
        assert (
            delete_response.status_code == 404
        ), f"Ожидался 404, получен {delete_response.status_code}"
        assert (
            error_code == expected_error
        ), f"Неверный код ошибки. Ожидался '{expected_error}', получен '{error_code}'"


@allure.epic("Yandex Disk API")
@allure.feature("Корзина и Восстановление")
@allure.story("Восстановление ресурсов")
@allure.title("TC-D4-06: Восстановление несуществующего ресурса")
@allure.description("Попытка восстановления папки, которой нет в корзине")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "trash", "restore")
def test_tc6_restore_non_existent_resource(yandex_client):
    non_existent_folder = f"Ghost_Folder_{fake.uuid4()}"

    with allure.step(
        f"Отправить запрос на восстановление несуществующей папки {non_existent_folder}"
    ):
        restore_response = yandex_client.restore_resource(non_existent_folder)
        attach_api_response(restore_response, expected_status=404)

    with allure.step("Проверить статус 404 и код ошибки DiskNotFoundError"):
        assert (
            restore_response.status_code == 404
        ), f"Ожидался статус 404 Not Found, получен {restore_response.status_code}"

        data = restore_response.json()
        error_code = data.get("error")

        expected_error = "DiskNotFoundError"
        attach_validation_result("Error Code", expected_error, error_code)

        assert (
            error_code == expected_error
        ), f"Неверный код ошибки. Ожидался '{expected_error}', получен '{error_code}'"

        assert "message" in data, "В ответе нет поля message"
        assert "description" in data, "В ответе нет поля description"
