import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import allure
from utils.data import ApiData


class TestDeleteCourier:

    @allure.title("Позитивное тестирование удаления курьера по id")
    def test_delete_courier_success(self, api, create_courier_fixture):
        courier_id = create_courier_fixture["id"]

        delete_response = api.delete(f"{ApiData.courier_endpoint}/{courier_id}")
        assert delete_response.status_code == 200

        del_res = delete_response.json()
        assert del_res == ApiData.ok_message

    @allure.title("Тестирование удаления курьера с несуществующим id")
    def test_delete_courier_without_id(self, api):

        id = "0"

        delete_responce = api.delete(ApiData.courier_endpoint + f"/{id}")

        assert delete_responce.status_code == 404

        dr = delete_responce.json()

        assert dr["message"] == ApiData.no_courier_with_that_id
