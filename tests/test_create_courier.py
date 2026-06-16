import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
import allure
from utils.data import ApiData


class TestCreateCourier:

    @allure.title("Позитивное тестирование регистрации курьера")
    def test_create_courier_success(self, api):
        payload = api.create_courier()

        responce = api.post(ApiData.courier_endpoint, data=payload)

        assert responce.status_code == 201

        r = responce.json()
        assert r == ApiData.ok_message

        login_payload = {"login": payload["login"], "password": payload["password"]}
        login_responce = api.post(ApiData.courier_login_endpoint, data=login_payload)
        id = login_responce.json()["id"]

        api.delete_courier(id)

    @allure.title("Тестирование создания дубликата курьера")
    def test_create_duplicate_courier(self, api, create_courier_fixture):
        payload = {
            "login": create_courier_fixture["login"],
            "password": create_courier_fixture["password"],
            "firstName": create_courier_fixture["firstName"],
        }

        second_responce = api.post(ApiData.courier_endpoint, data=payload)
        assert second_responce.status_code == 409

        sr = second_responce.json()
        assert sr["message"] == ApiData.login_already_used

    @allure.title(
        "Тестирование регистрации курьера без заполнения одного из обязательных полей"
    )
    @pytest.mark.parametrize(
        "missing_field, error_message",
        [
            ("login", ApiData.not_enough_data_to_create_account),
            ("password", ApiData.not_enough_data_to_create_account),
        ],
    )
    def test_create_courier_without_required_field(
        self, missing_field, error_message, api
    ):
        payload = api.create_courier()

        del payload[missing_field]

        responce = api.post(ApiData.courier_endpoint, data=payload)
        assert responce.status_code == 400

        r = responce.json()
        assert r["message"] == error_message
