import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import allure
from utils.data import ApiData


class TestGetOrder:

    @allure.title("Тестирование получения списка заказов без id курьера")
    def test_get_orders(self, api):

        response = api.get(ApiData.orders_endpoint)

        assert response.status_code == 200

        r = response.json()

        assert len(r["orders"]) > 0

    @allure.title("Тестирование получения заказа по track номеру")
    def test_get_orders_by_track(self, api):

        order_data = api.create_order()

        responce = api.post(ApiData.orders_endpoint, data=order_data)

        r = responce.json()

        track = r["track"]

        get_by_track_response = api.get(
            ApiData.orders_endpoint + f"/track?t={str(track)}"
        )

        assert get_by_track_response.status_code == 200

        gbtr = get_by_track_response.json()

        assert "order" in gbtr

        api.cancel_order(track)
