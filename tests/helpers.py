from random import randint
from faker import Faker

faker = Faker()
BASE_URL = "https://qa-internship.avito.com"


def random_seller_id():
    return randint(111111, 999999)


def generate_payload(**overrides):
    payload = {
        "sellerID": random_seller_id(),
        "name": faker.word(),
        "price": randint(1, 100000),
        "statistics": {"likes": randint(0, 100), "viewCount": randint(0, 1000), "contacts": randint(0, 100)},
    }
    payload.update(overrides)
    return payload
