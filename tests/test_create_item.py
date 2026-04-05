import allure
import pytest
from utils.api_client import ApiClient
from utils.helpers import generate_payload

api = ApiClient()


@allure.title("Успешное создание объявления с валидными данными")
@allure.description("Проверяем что POST /api/1/item возвращает 200 и поле id в ответе")
@allure.severity(allure.severity_level.BLOCKER)
def test_create_item_success():  # TC-001
    payload = generate_payload()

    with allure.step("Отправляем POST /api/1/item с валидными данными"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 200"):
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
    with allure.step("Проверяем наличие поля id в ответе"):
        assert "id" in data, "В ответе отсутствует поле id"


@allure.title("Создание объявления с price = 0")
@allure.description("Нулевая цена должна быть допустима — ожидаем 200")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_price_zero():  # TC-002
    payload = generate_payload(price=0)

    with allure.step("Отправляем POST /api/1/item с price = 0"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 200"):
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"


@allure.title("Создание объявления с price = -1")
@allure.description("Отрицательная цена недопустима — ожидаем 400")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_negative_price():  # TC-003
    payload = generate_payload(price=-1)

    with allure.step("Отправляем POST /api/1/item с price = -1"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления без поля name")
@allure.description("Отсутствие обязательного поля name — ожидаем 400")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_item_without_name():  # TC-004
    payload = generate_payload()
    payload.pop("name")

    with allure.step("Отправляем POST /api/1/item без поля name"):
        response = api.create_item(payload)
        data = response.json()

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления без поля price")
@allure.description("Отсутствие обязательного поля price — ожидаем 400")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_item_without_price():  # TC-005
    payload = generate_payload()
    payload.pop("price")

    with allure.step("Отправляем POST /api/1/item без поля price"):
        response = api.create_item(payload)
        data = response.json()

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления без поля sellerID")
@allure.description("Отсутствие обязательного поля sellerID — ожидаем 400")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_item_without_seller():  # TC-006
    payload = generate_payload()
    payload.pop("sellerID")

    with allure.step("Отправляем POST /api/1/item без поля sellerID"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления без поля statistics")
@allure.description("Отсутствие поля statistics — ожидаем 400")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_item_without_statistics():  # TC-007
    payload = generate_payload()
    payload.pop("statistics")

    with allure.step("Отправляем POST /api/1/item без поля statistics"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления с пустым телом запроса")
@allure.description("Пустое тело запроса — ожидаем 400")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_item_without_body():  # TC-008
    with allure.step("Отправляем POST /api/1/item с пустым телом"):
        response = api.create_item({})
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления с name из 1 символа")
@allure.description("Минимально короткое имя — ожидаем 200")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_short_name():  # TC-009
    payload = generate_payload(name="S")

    with allure.step("Отправляем POST /api/1/item с name = 'S'"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 200"):
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"


@allure.title("Создание объявления с пустым name")
@allure.description("Пустое имя недопустимо — ожидаем 400")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_with_empty_name():  # TC-010
    payload = generate_payload(name="")

    with allure.step("Отправляем POST /api/1/item с name = ''"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления с XSS в поле name")
@allure.description("XSS-скрипт в name должен отклоняться — ожидаем 400")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_item_with_special_chars_name():  # TC-011
    payload = generate_payload(name='<script>alert("hack")</script>')

    with allure.step("Отправляем POST /api/1/item с XSS в поле name"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления со строковым sellerID")
@allure.description("Строка в поле sellerID недопустима — ожидаем 400")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_with_string_seller_id():  # TC-012
    payload = generate_payload(sellerID="десять тысяч сто двадцать один")

    with allure.step("Отправляем POST /api/1/item со строковым sellerID"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Идемпотентность — два одинаковых POST дают разные id")
@allure.description("Повторный запрос с тем же телом должен создавать новое объявление с уникальным id")
@allure.severity(allure.severity_level.MINOR)
def test_create_items_with_same_body():  # TC-013
    payload = generate_payload()

    with allure.step("Отправляем первый POST /api/1/item"):
        response1 = api.create_item(payload)
        data1 = response1.json()

    with allure.step("Отправляем второй POST /api/1/item с тем же телом"):
        response2 = api.create_item(payload)
        data2 = response2.json()

    item_id1 = data1["status"].split(" - ")[-1]
    item_id2 = data2["status"].split(" - ")[-1]

    if response1.status_code == 200:
        api.delete_item(item_id1)
    if response2.status_code == 200:
        api.delete_item(item_id2)

    with allure.step("Проверяем что оба запроса вернули 200"):
        assert response1.status_code == 200, f"Первый запрос: ожидали 200, получили {response1.status_code}"
        assert response2.status_code == 200, f"Второй запрос: ожидали 200, получили {response2.status_code}"
    with allure.step("Проверяем что id объявлений различаются"):
        assert item_id1 != item_id2, f"Ожидали разные id, получили одинаковые: {item_id1}"


@allure.title("Создание объявления с дробным price")
@allure.description("Дробная цена недопустима — ожидаем 400")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_with_float_price():  # TC-014
    payload = generate_payload(price=99.99)

    with allure.step("Отправляем POST /api/1/item с price = 99.99"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления с очень большим price")
@allure.description("Граничное значение — очень большое число в поле price, ожидаем 200 или 400")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_with_very_large_price():  # TC-015
    payload = generate_payload(price=9999999999)

    with allure.step("Отправляем POST /api/1/item с price = 9999999999"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем что сервис не вернул 500"):
        assert response.status_code != 500, f"Сервис вернул 500 Internal Server Error. Ответ: {data}"


@allure.title("Создание объявления с очень длинным name")
@allure.description("Граничное значение — name из 10000 символов, ожидаем 200 или 400, но не 500")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_with_very_long_name():  # TC-016
    payload = generate_payload(name="a" * 10000)

    with allure.step("Отправляем POST /api/1/item с name из 10000 символов"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем что сервис не вернул 500"):
        assert response.status_code != 500, f"Сервис вернул 500 Internal Server Error. Ответ: {data}"


@allure.title("Создание объявления с sellerID = 0")
@allure.description("Граничное значение sellerID — ожидаем 400")
@allure.severity(allure.severity_level.MINOR)
def test_create_item_with_seller_id_zero():  # TC-017
    payload = generate_payload(sellerID=0)

    with allure.step("Отправляем POST /api/1/item с sellerID = 0"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"

@allure.title("Создание объявления с невалидными значениями в statistics: {stat_field} = {stat_value}")
@allure.description("Отрицательные значения в полях statistics недопустимы — ожидаем 400")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("stat_field,stat_value", [
    ("likes", -1),
    ("viewCount", -1),
    ("contacts", -1),
])
def test_create_item_with_negative_statistics(stat_field, stat_value):  # TC-018
    statistics = {"likes": 0, "viewCount": 0, "contacts": 0}
    statistics[stat_field] = stat_value
    payload = generate_payload(statistics=statistics)

    with allure.step(f"Отправляем POST /api/1/item с {stat_field} = {stat_value}"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"


@allure.title("Создание объявления с отсутствующим полем в statistics: без {missing_field}")
@allure.description("Отсутствие обязательного поля внутри statistics — ожидаем 400")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("missing_field", ["likes", "viewCount", "contacts"])
def test_create_item_with_missing_statistics_field(missing_field):  # TC-019
    statistics = {"likes": 1, "viewCount": 2, "contacts": 1}
    statistics.pop(missing_field)
    payload = generate_payload(statistics=statistics)

    with allure.step(f"Отправляем POST /api/1/item без поля statistics.{missing_field}"):
        response = api.create_item(payload)
        data = response.json()

    if response.status_code == 200:
        item_id = data["status"].split(" - ")[-1]
        with allure.step(f"Удаляем созданное объявление {item_id}"):
            api.delete_item(item_id)

    with allure.step("Проверяем статус 400"):
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Ответ: {data}"
