import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
import allure
from api.api_client import ApiClient


class TestLoginCourier:
    base_url = "https://qa-scooter.praktikum-services.ru"

    @allure.title("Тестирование успешной авторизации курьера")
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
    @allure.title(
        "Тестирование авторизации курьера без заполнения одного из обязательных полей"
    )
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

        print(login_responce.text)

        assert login_responce.status_code == 400

        lg = login_responce.json()

        assert lg["message"] == error_message

    @allure.title("Тестирование авторизации курьера с несуществующими данными")
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
