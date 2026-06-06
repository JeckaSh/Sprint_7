import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
import allure
from api.api_client import ApiClient


class TestCreateOrder:
    base_url = "https://qa-scooter.praktikum-services.ru"

    @allure.title("Позитивное тестирование создания заказа")
    def test_create_order(self):
        api = ApiClient(self.base_url)

        order_data = {
            "firstName": "Naruto123",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
        }

        responce = api.post("/api/v1/orders", data=order_data)
        assert responce.status_code == 201

        r = responce.json()

        assert "track" in r

    @allure.title("Тестирование создания заказа с указанием разных параметров color")
    @pytest.mark.parametrize(
        "color_data",
        [
            ([]),
            (["BLACK"]),
            (["GREY"]),
            (["BLACK", "GREY"]),
        ],
    )
    def test_create_order_with_color(self, color_data):
        api = ApiClient(self.base_url)

        color = []
        color = color.append(color_data)

        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color,
        }

        responce = api.post("/api/v1/orders", data=order_data)

        assert responce.status_code == 201

        r = responce.json()

        assert "track" in r
