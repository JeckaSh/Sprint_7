import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
import allure
from utils.data import ApiData


class TestCreateOrder:

    @allure.title("Позитивное тестирование создания заказа")
    def test_create_order(self, api):

        order_data = api.create_order()

        responce = api.post(ApiData.orders_endpoint, data=order_data)
        assert responce.status_code == 201

        r = responce.json()

        assert "track" in r

        api.cancel_order(r["track"])

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
    def test_create_order_with_color(self, color_data, api):

        color = []
        color = color.append(color_data)

        order_data = api.create_order_with_color(color)

        responce = api.post(ApiData.orders_endpoint, data=order_data)

        assert responce.status_code == 201

        r = responce.json()

        assert "track" in r

        api.cancel_order(r["track"])
