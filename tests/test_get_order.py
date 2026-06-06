import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import allure
from api.api_client import ApiClient


class TestGetOrder:
    base_url = "https://qa-scooter.praktikum-services.ru"

    @allure.title("Тестирование получения списка заказов без id курьера")
    def test_get_orders(self):
        api = ApiClient(self.base_url)

        response = api.get("/api/v1/orders")

        assert response.status_code == 200

        r = response.json()

        assert len(r["orders"]) > 0

    @allure.title("Тестирование получения заказа по track номеру")
    def test_get_orders_by_track(self):
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

        track = r["track"]

        get_by_track_response = api.get("/api/v1/orders/track?t=" + str(track))

        assert get_by_track_response.status_code == 200

        gbtr = get_by_track_response.json()

        assert "order" in gbtr
