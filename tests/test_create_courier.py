import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
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

    # создание курьера без заполнения обязательных полей
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
