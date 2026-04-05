import pytest
from utils.api_client import ApiClient
from utils.helpers import generate_payload


@pytest.fixture
def api():
    return ApiClient()


@pytest.fixture
def create_and_delete_item(api):
    payload = generate_payload()

    response = api.create_item(payload)
    data = response.json()
    if "id" in data:
        item_id = data["id"]
    else:
        item_id = data["status"].split(" - ")[-1]

    yield {"id": item_id, "payload": payload}

    api.delete_item(item_id)
