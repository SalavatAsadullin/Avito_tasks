import allure
from utils.api_client import ApiClient

api = ApiClient()


@allure.title("Получение статистики по существующему объявлению (v1)")
@allure.description("Проверяем что GET /api/1/statistic/{id} возвращает корректные данные")
@allure.severity(allure.severity_level.BLOCKER)
def test_get_statistic(create_and_delete_item):  # TC-022
    item_id = create_and_delete_item["id"]
    payload = create_and_delete_item["payload"]

    with allure.step(f"Отправляем GET /api/1/statistic/{item_id}"):
        response = api.get_statistic_v1(item_id)
        data = response.json()

    with allure.step("Проверяем статус 200 и структуру ответа"):
        assert response.status_code == 200, f"Ожидали 200, получили: {response.status_code}. Ответ {data}"
        assert isinstance(data, list), "Ответ должен быть списком"
        assert len(data) > 0, "Список статистики не должен быть пустым"

    with allure.step("Проверяем поля и значения статистики"):
        items = data[0]
        assert "likes" in items, "В ответе нет поля likes"
        assert "viewCount" in items, "В ответе нет поля viewCount"
        assert "contacts" in items, "В ответе нет поля contacts"
        assert items["likes"] == payload["statistics"]["likes"], "likes не совпадает"
        assert items["viewCount"] == payload["statistics"]["viewCount"], "viewCount не совпадает"
        assert items["contacts"] == payload["statistics"]["contacts"], "contacts не совпадает"


@allure.title("Получение статистики по существующему объявлению (v2)")
@allure.description("Проверяем что GET /api/2/statistic/{id} возвращает корректные данные")
@allure.severity(allure.severity_level.BLOCKER)
def test_get_statistic_v2(create_and_delete_item):  # TC-023
    item_id = create_and_delete_item["id"]
    payload = create_and_delete_item["payload"]

    with allure.step(f"Отправляем GET /api/2/statistic/{item_id}"):
        response = api.get_statistic_v2(item_id)
        data = response.json()

    with allure.step("Проверяем статус 200 и структуру ответа"):
        assert response.status_code == 200, f"Ожидали 200, получили: {response.status_code}. Ответ: {data}"
        assert isinstance(data, list), "Ответ должен быть списком"
        assert len(data) > 0, "Список статистики не должен быть пустым"

    with allure.step("Проверяем поля и значения статистики"):
        stat = data[0]
        assert "likes" in stat, "В ответе нет поля likes"
        assert "viewCount" in stat, "В ответе нет поля viewCount"
        assert "contacts" in stat, "В ответе нет поля contacts"
        assert stat["likes"] == payload["statistics"]["likes"], "likes не совпадает"
        assert stat["viewCount"] == payload["statistics"]["viewCount"], "viewCount не совпадает"
        assert stat["contacts"] == payload["statistics"]["contacts"], "contacts не совпадает"


@allure.title("Данные статистики v1 и v2 совпадают")
@allure.description("Проверяем консистентность данных между /api/1/statistic и /api/2/statistic")
@allure.severity(allure.severity_level.NORMAL)
def test_compare_statistic_v1_v2(create_and_delete_item):  # TC-024
    item_id = create_and_delete_item["id"]

    with allure.step(f"Получаем статистику v1 для {item_id}"):
        response_v1 = api.get_statistic_v1(item_id)
        data_v1 = response_v1.json()

    with allure.step(f"Получаем статистику v2 для {item_id}"):
        response_v2 = api.get_statistic_v2(item_id)
        data_v2 = response_v2.json()

    with allure.step("Проверяем что оба запроса вернули 200"):
        assert response_v1.status_code == 200, f"v1 вернул {response_v1.status_code}"
        assert response_v2.status_code == 200, f"v2 вернул {response_v2.status_code}"

    with allure.step("Сравниваем значения статистики v1 и v2"):
        stat_v1 = data_v1[0]
        stat_v2 = data_v2[0]
        assert stat_v1["likes"] == stat_v2["likes"], (
            f"likes отличается: v1={stat_v1['likes']}, v2={stat_v2['likes']}"
        )
        assert stat_v1["viewCount"] == stat_v2["viewCount"], (
            f"viewCount отличается: v1={stat_v1['viewCount']}, v2={stat_v2['viewCount']}"
        )
        assert stat_v1["contacts"] == stat_v2["contacts"], (
            f"contacts отличается: v1={stat_v1['contacts']}, v2={stat_v2['contacts']}"
        )


@allure.title("Получение статистики по несуществующему id (v1)")
@allure.description("Запрос с несуществующим UUID — ожидаем 404")
@allure.severity(allure.severity_level.NORMAL)
def test_get_statistic_non_existent_id_v1():  # TC-025
    with allure.step("Отправляем GET /api/1/statistic с несуществующим UUID"):
        response = api.get_statistic_v1("00000000-0000-0000-0000-000000000000")
        data = response.json()

    with allure.step("Проверяем статус 404"):
        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
    with allure.step("Проверяем тело ошибки"):
        assert "result" in data or "status" in data, "Тело ошибки не содержит ожидаемых полей"


@allure.title("Получение статистики по несуществующему id (v2)")
@allure.description("Запрос с несуществующим UUID — ожидаем 404")
@allure.severity(allure.severity_level.NORMAL)
def test_get_statistic_non_existent_id_v2():  # TC-026
    with allure.step("Отправляем GET /api/2/statistic с несуществующим UUID"):
        response = api.get_statistic_v2("00000000-0000-0000-0000-000000000000")
        data = response.json()

    with allure.step("Проверяем статус 404"):
        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
    with allure.step("Проверяем тело ошибки"):
        assert "result" in data or "status" in data, "Тело ошибки не содержит ожидаемых полей"
