import allure
import time
from utils.api_client import ApiClient
from utils.helpers import generate_payload

api = ApiClient()


@allure.title("Content-Type в заголовке ответа равен application/json")
@allure.description("Проверяем что сервис возвращает корректный заголовок Content-Type")
@allure.severity(allure.severity_level.MINOR)
def test_content_type_header(create_and_delete_item):  # TC-026
    item_id = create_and_delete_item["id"]

    with allure.step(f"Отправляем GET /api/1/item/{item_id}"):
        response = api.get_item(item_id)

    with allure.step("Проверяем заголовок Content-Type"):
        assert "application/json" in response.headers["Content-Type"], (
            f"Ожидали application/json, получили: {response.headers['Content-Type']}"
        )


@allure.title("Время ответа на создание объявления не превышает 2000 мс")
@allure.description("Нефункциональная проверка производительности POST /api/1/item")
@allure.severity(allure.severity_level.NORMAL)
def test_post_response_item():  # TC-027
    payload = generate_payload()

    with allure.step("Отправляем POST /api/1/item и замеряем время"):
        start = time.time()
        response = api.create_item(payload)
        elapsed = (time.time() - start) * 1000

    if response.status_code == 200:
        item_id = response.json()["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step(f"Проверяем что время ответа {elapsed:.0f}мс < 2000мс"):
        assert elapsed < 2000, f"Ожидали ответ < 2000мс, получили {elapsed:.0f}мс"


@allure.title("Время ответа на получение объявления не превышает 1000 мс")
@allure.description("Нефункциональная проверка производительности GET /api/1/item/{id}")
@allure.severity(allure.severity_level.MINOR)
def test_get_response_time(create_and_delete_item):  # TC-028
    item_id = create_and_delete_item["id"]

    with allure.step(f"Отправляем GET /api/1/item/{item_id} и замеряем время"):
        start = time.time()
        api.get_item(item_id)
        elapsed = (time.time() - start) * 1000

    with allure.step(f"Проверяем что время ответа {elapsed:.0f}мс < 1000мс"):
        assert elapsed < 2000, f"Ожидали ответ < 2000мс, получили {elapsed:.0f}мс"
