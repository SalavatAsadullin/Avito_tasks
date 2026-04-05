import allure
from utils.api_client import ApiClient
from utils.helpers import random_seller_id, generate_payload

api = ApiClient()


@allure.title("Успешное получение объявления по id")
@allure.description("Проверяем что GET /api/1/item/{id} возвращает корректные данные")
@allure.severity(allure.severity_level.BLOCKER)
def test_get_item(create_and_delete_item):  # TC-015
    item_id = create_and_delete_item["id"]
    payload = create_and_delete_item["payload"]

    with allure.step(f"Отправляем GET /api/1/item/{item_id}"):
        response = api.get_item(item_id)
        data = response.json()

    with allure.step("Проверяем статус 200"):
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
    with allure.step("Проверяем что ответ не пустой"):
        assert len(data) > 0, "Ответ пришёл пустым списком"

    item = data[0]
    with allure.step("Проверяем поля объявления"):
        assert item.get("createdAt"), "Поле createdAt отсутствует или пустое"
        assert item["id"] == item_id, "id не совпадает"
        assert item["name"] == payload["name"], "name не совпадает"
        assert item["price"] == payload["price"], "price не совпадает"
        assert item["sellerId"] == payload["sellerID"], "sellerId не совпадает"
        assert item["statistics"]["likes"] == payload["statistics"]["likes"], "likes не совпадает"
        assert item["statistics"]["viewCount"] == payload["statistics"]["viewCount"], "viewCount не совпадает"
        assert item["statistics"]["contacts"] == payload["statistics"]["contacts"], "contacts не совпадает"


@allure.title("Получение объявления по несуществующему id")
@allure.description("Запрос с несуществующим UUID — ожидаем 404")
@allure.severity(allure.severity_level.MINOR)
def test_get_item_with_non_existent_id():  # TC-016
    with allure.step("Отправляем GET /api/1/item с несуществующим UUID"):
        response = api.get_item("00000000-0000-0000-0000-000000000000")

    with allure.step("Проверяем статус 404"):
        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"


@allure.title("Получение объявления по невалидному id")
@allure.description("Запрос с невалидным id (не UUID) — ожидаем 400 или 404")
@allure.severity(allure.severity_level.MINOR)
def test_get_item_with_invalid_id():  # TC-017
    with allure.step("Отправляем GET /api/1/item с невалидным id 'abcd'"):
        response = api.get_item("abcd")

    with allure.step("Проверяем статус 400 или 404"):
        assert response.status_code in [400, 404], (
            f"Ожидали 404 или 400, получили {response.status_code}"
        )


@allure.title("Получение всех объявлений продавца")
@allure.description("Создаём два объявления одному продавцу и проверяем что оба есть в списке")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_seller_items():  # TC-018
    seller_id = random_seller_id()

    with allure.step(f"Создаём два объявления для продавца {seller_id}"):
        payload1 = generate_payload(sellerID=seller_id)
        payload2 = generate_payload(sellerID=seller_id)
        response1 = api.create_item(payload1)
        response2 = api.create_item(payload2)
        id_1 = response1.json()["status"].split(" - ")[-1]
        id_2 = response2.json()["status"].split(" - ")[-1]

    with allure.step(f"Получаем список объявлений продавца {seller_id}"):
        response = api.get_seller_items(seller_id)
        data = response.json()

    api.delete_item(id_1)
    api.delete_item(id_2)

    with allure.step("Проверяем статус 200 и структуру ответа"):
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        assert isinstance(data, list), "Ответ должен быть списком"
        assert len(data) > 0, f"Ожидали минимум 1 объявление, получили {len(data)}"

    with allure.step("Проверяем поля каждого элемента"):
        for item in data:
            assert "id" in item, "В элементе нет поля id"
            assert "sellerId" in item, "В элементе нет поля sellerId"
            assert "name" in item, "В элементе нет поля name"
            assert "price" in item, "В элементе нет поля price"
            assert "statistics" in item, "В элементе нет поля statistics"
            assert "createdAt" in item, "В элементе нет поля createdAt"
            assert item["sellerId"] == seller_id, "sellerId не совпадает"

    with allure.step("Проверяем что оба созданных объявления есть в списке"):
        ids_in_response = [item["id"] for item in data]
        assert id_1 in ids_in_response, f"id_1 {id_1} не найден в списке"
        assert id_2 in ids_in_response, f"id_2 {id_2} не найден в списке"


@allure.title("Получение объявлений продавца без объявлений")
@allure.description("Продавец без объявлений — ожидаем 200 с пустым списком или 404")
@allure.severity(allure.severity_level.MINOR)
def test_get_seller_items_empty():  # TC-019
    seller_id = 12412421

    with allure.step(f"Отправляем GET /api/1/{seller_id}/item"):
        response = api.get_seller_items(seller_id)
        data = response.json()

    with allure.step("Проверяем статус 200 или 404"):
        assert response.status_code in [200, 404], (
            f"Ожидали 200 или 404, получили {response.status_code}"
        )
    if response.status_code == 200:
        with allure.step("Проверяем что список пустой"):
            assert isinstance(data, list), "Ответ должен быть списком"
            assert len(data) == 0, f"Ожидали пустой список, получили {len(data)} элементов"


@allure.title("Получение объявлений со строковым sellerID")
@allure.description("Строка вместо числа в пути — ожидаем 400 или 404")
@allure.severity(allure.severity_level.MINOR)
def test_get_items_with_string_seller_id():  # TC-020
    seller_id = "skakskdkds"

    with allure.step(f"Отправляем GET /api/1/{seller_id}/item"):
        response = api.get_seller_items(seller_id)
        data = response.json()

    with allure.step("Проверяем статус 400 или 404"):
        assert response.status_code in [400, 404], (
            f"Ожидали 400 или 404, получили {response.status_code}. Ответ: {data}"
        )


@allure.title("Объявление продавца A отсутствует в списке продавца B")
@allure.description("Проверяем изоляцию данных между продавцами")
@allure.severity(allure.severity_level.CRITICAL)
def test_item_not_in_another_seller_list():  # TC-021
    seller_a = random_seller_id()
    seller_b = random_seller_id()

    with allure.step(f"Создаём объявление для продавца A ({seller_a})"):
        payload = generate_payload(sellerID=seller_a)
        response = api.create_item(payload)
        id_a = response.json()["status"].split(" - ")[-1]

    with allure.step(f"Получаем список объявлений продавца B ({seller_b})"):
        response_b = api.get_seller_items(seller_b)
        data_b = response_b.json()

    api.delete_item(id_a)

    with allure.step("Проверяем что объявление A не попало в список B"):
        if isinstance(data_b, list):
            ids_in_b = [item["id"] for item in data_b]
            assert id_a not in ids_in_b, "Объявление продавца A найдено в списке продавца B"
        else:
            assert False, f"Ожидали список в ответе, получили: {type(data_b)}, тело: {data_b}"
