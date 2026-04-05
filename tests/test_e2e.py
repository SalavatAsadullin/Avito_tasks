import allure
from utils.api_client import ApiClient
from utils.helpers import generate_payload

api = ApiClient()


@allure.title("Полный жизненный цикл объявления")
@allure.description(
    "E2E TC-E01: POST /item → GET /item/{id} → GET /statistic/{id} → DELETE /item/{id}. "
    "Проверяем консистентность данных во всех ручках."
)
@allure.severity(allure.severity_level.BLOCKER)
def test_full_item_lifecycle():
    payload = generate_payload()

    with allure.step("Создаём объявление POST /api/1/item"):
        post_response = api.create_item(payload)
        assert post_response.status_code == 200, (
            f"[POST] Ожидали 200, получили {post_response.status_code}"
        )
        item_id = post_response.json()["status"].split(" - ")[-1]

    try:
        with allure.step(f"Получаем объявление GET /api/1/item/{item_id}"):
            get_response = api.get_item(item_id)
            assert get_response.status_code == 200, (
                f"[GET /item] Ожидали 200, получили {get_response.status_code}"
            )
            item_data = get_response.json()
            assert len(item_data) > 0, "[GET /item] Ответ пришёл пустым списком"

        with allure.step("Проверяем поля объявления совпадают с переданными при создании"):
            item = item_data[0]
            assert item["id"] == item_id, "id не совпадает"
            assert item["name"] == payload["name"], "name не совпадает"
            assert item["price"] == payload["price"], "price не совпадает"
            assert item["sellerId"] == payload["sellerID"], "sellerId не совпадает"

        with allure.step(f"Получаем статистику GET /api/1/statistic/{item_id}"):
            stat_response = api.get_statistic_v1(item_id)
            assert stat_response.status_code == 200, (
                f"[GET /statistic] Ожидали 200, получили {stat_response.status_code}"
            )
            stat_data = stat_response.json()
            assert len(stat_data) > 0, "[GET /statistic] Список статистики пустой"

        with allure.step("Проверяем статистику совпадает с переданной при создании"):
            stat = stat_data[0]
            assert stat["likes"] == payload["statistics"]["likes"], (
                f"likes не совпадает: ожидали {payload['statistics']['likes']}, получили {stat['likes']}"
            )
            assert stat["viewCount"] == payload["statistics"]["viewCount"], (
                f"viewCount не совпадает: ожидали {payload['statistics']['viewCount']}, получили {stat['viewCount']}"
            )
            assert stat["contacts"] == payload["statistics"]["contacts"], (
                f"contacts не совпадает: ожидали {payload['statistics']['contacts']}, получили {stat['contacts']}"
            )

        with allure.step("Проверяем консистентность статистики между /item и /statistic"):
            assert item["statistics"]["likes"] == stat["likes"], (
                "likes расходится между /item и /statistic"
            )
            assert item["statistics"]["viewCount"] == stat["viewCount"], (
                "viewCount расходится между /item и /statistic"
            )
            assert item["statistics"]["contacts"] == stat["contacts"], (
                "contacts расходится между /item и /statistic"
            )

    finally:
        with allure.step(f"Удаляем объявление DELETE /api/2/item/{item_id}"):
            api.delete_item(item_id)
