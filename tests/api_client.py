import requests
from utils.helpers import BASE_URL


class ApiClient:
    def create_item(self, payload):
        return requests.post(f"{BASE_URL}/api/1/item", json=payload)

    def get_item(self, item_id):
        return requests.get(f"{BASE_URL}/api/1/item/{item_id}")

    def get_seller_items(self, seller_id):
        return requests.get(f"{BASE_URL}/api/1/{seller_id}/item")

    def get_statistic_v1(self, item_id):
        return requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")

    def get_statistic_v2(self, item_id):
        return requests.get(f"{BASE_URL}/api/2/statistic/{item_id}")

    def delete_item(self, item_id):
        return requests.delete(f"{BASE_URL}/api/2/item/{item_id}")
