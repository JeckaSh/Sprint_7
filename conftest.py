import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest

from api.api_client import ApiClient
from utils.data import ApiData


@pytest.fixture()
def api():
    api = ApiClient(ApiData.base_url)

    yield api

    api.session.close()


@pytest.fixture()
def create_courier_fixture(api):
    data = api.create_courier()
    create_response = api.post(ApiData.courier_endpoint, data=data)

    login_data = {"login": data["login"], "password": data["password"]}
    login_response = api.post(ApiData.courier_login_endpoint, data=login_data)

    courier_id = str(login_response.json()["id"])

    # данные для использования в тестах
    courier_data = {
        "login": data["login"],
        "password": data["password"],
        "firstName": data["firstName"],
        "id": courier_id,
    }

    yield courier_data

    delete_response = api.delete(f"{ApiData.courier_endpoint}/{courier_data["id"]}")


@pytest.fixture()
def create_order_fixture(api):
    order_data = api.create_order()
    response = api.post(ApiData.orders_endpoint, data=order_data)

    order = response.json()
    track = order["track"]

    yield {"data": order_data, "response": order, "track": track}

    cancel_order = api.cancel_order(track)
