import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
import allure
from utils.data import ApiData


class TestLoginCourier:

    @allure.title("Тестирование успешной авторизации курьера")
    def test_login_courier_success(self, api):
        payload = api.create_courier()

        responce = api.post(ApiData.courier_endpoint, data=payload)

        login_payload = {"login": payload["login"], "password": payload["password"]}

        login_responce = api.post(ApiData.courier_login_endpoint, data=login_payload)

        assert login_responce.status_code == 200

        lg = login_responce.json()
        assert "id" in lg

        api.delete_courier(lg["id"])

    @allure.title(
        "Тестирование авторизации курьера без заполнения одного из обязательных полей"
    )
    @pytest.mark.parametrize(
        "missing_field, error_message",
        [
            ("login", ApiData.not_enough_data_to_login),
        ],
    )
    def test_login_courier_without_required_field(
        self, missing_field, error_message, api
    ):
        payload = api.create_courier()

        responce = api.post(ApiData.courier_endpoint, data=payload)

        login_payload = {"login": payload["login"], "password": payload["password"]}

        del login_payload[missing_field]

        login_responce = api.post(ApiData.courier_login_endpoint, data=login_payload)

        assert login_responce.status_code == 400

        lg = login_responce.json()

        assert lg["message"] == error_message

    @allure.title("Тестирование авторизации курьера с несуществующими данными")
    def test_courier_login_nonexistent_data(self, api):
        payload = api.create_courier()

        responce = api.post(ApiData.courier_endpoint, data=payload)

        login_payload = {
            "login": payload["login"] + "data",
            "password": payload["password"] + "data",
        }

        login_responce = api.post(ApiData.courier_login_endpoint, data=login_payload)

        assert login_responce.status_code == 404

        lg = login_responce.json()

        assert lg["message"] == ApiData.user_not_found
