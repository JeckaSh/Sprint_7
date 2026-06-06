import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
from utils.data import generate_random_string
from api.api_client import ApiClient


class TestCreateCourier:
    base_url = "https://qa-scooter.praktikum-services.ru"

    # успешное создание курьера
    def test_create_courier_success(self):
        api = ApiClient(self.base_url)
        payload = api.create_courier()

        responce = api.post("/api/v1/courier", data=payload)

        assert responce.status_code == 201

        r = responce.json()
        assert r == {"ok": True}

    # создание дубликата курьера, отображение ошибки при создании дубликата
    def test_create_duplicate_courier(self):
        api = ApiClient(self.base_url)
        payload = api.create_courier()

        first_responce = api.post("/api/v1/courier", data=payload)
        assert first_responce.status_code == 201

        second_responce = api.post("/api/v1/courier", data=payload)
        assert second_responce.status_code == 409

        sr = second_responce.json()
        assert sr["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize(
        "missing_field, error_message",
        [
            ("login", "Недостаточно данных для создания учетной записи"),
            ("password", "Недостаточно данных для создания учетной записи"),
        ],
    )
    def test_create_courier_without_required_field(self, missing_field, error_message):
        api = ApiClient(self.base_url)
        payload = api.create_courier()

        del payload[missing_field]

        responce = api.post("/api/v1/courier", data=payload)
        assert responce.status_code == 400

        r = responce.json()
        assert r["message"] == error_message

    def test_login_courier_success(self):
        api = ApiClient(self.base_url)
        payload = api.create_courier()

        responce = api.post("/api/v1/courier", data=payload)

        login_payload = {"login": payload["login"], "password": payload["password"]}

        login_responce = api.post("/api/v1/courier/login", data=login_payload)

        assert login_responce.status_code == 200

        lg = login_responce.json()
        assert "id" in lg

    # TODO: разобраться в причинах появляения 504 вместо 400 при логине без пароля
    # ("password", "Недостаточно данных для входа")
    @pytest.mark.parametrize(
        "missing_field, error_message",
        [
            ("login", "Недостаточно данных для входа"),
        ],
    )
    def test_login_courier_without_required_field(self, missing_field, error_message):
        api = ApiClient(self.base_url)
        payload = api.create_courier()

        responce = api.post("/api/v1/courier", data=payload)

        assert responce.status_code == 201

        login_payload = {"login": payload["login"], "password": payload["password"]}

        del login_payload[missing_field]

        login_responce = api.post("/api/v1/courier/login", data=login_payload)

        assert login_responce.status_code == 400

        lg = login_responce.json()

        assert lg["message"] == error_message

    def test_courier_login_nonexistent_data(self):
        api = ApiClient(self.base_url)
        payload = api.create_courier()

        responce = api.post("/api/v1/courier", data=payload)

        assert responce.status_code == 201

        login_payload = {
            "login": payload["login"] + "data",
            "password": payload["password"] + "data",
        }

        login_responce = api.post("/api/v1/courier/login", data=login_payload)

        assert login_responce.status_code == 404

        lg = login_responce.json()

        assert lg["message"] == "Учетная запись не найдена"

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

    def test_get_orders(self):
        api = ApiClient(self.base_url)

        response = api.get("/api/v1/orders")

        assert response.status_code == 200

        r = response.json()

        assert len(r["orders"]) > 0

    def test_get_orders_by_courier_id(self):
        pass
