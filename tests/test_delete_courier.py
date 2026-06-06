import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from api.api_client import ApiClient


class TestDeleteCourier:
    base_url = "https://qa-scooter.praktikum-services.ru"

    # позитивный тест удаление курьера
    def test_delete_courier_success(self):
        # создать курьера
        api = ApiClient(self.base_url)
        payload = api.create_courier()

        responce = api.post("/api/v1/courier", data=payload)

        assert responce.status_code == 201

        # залогинить курьера для получения id
        login_payload = {"login": payload["login"], "password": payload["password"]}

        login_responce = api.post("/api/v1/courier/login", data=login_payload)

        assert login_responce.status_code == 200

        # удалть курьера по id
        lg = login_responce.json()

        courier_id = str(lg["id"])

        delete_courier_by_id_responce = api.delete("/api/v1/courier/" + courier_id)

        assert delete_courier_by_id_responce.status_code == 200

        del_res = delete_courier_by_id_responce.json()
        assert del_res == {"ok": True}

    # негативный тест удаление курьера с несуществующим id
    def test_delete_courier_without_id(self):
        api = ApiClient(self.base_url)

        id = "0"

        delete_responce = api.delete("/api/v1/courier/" + id)

        print(delete_responce)

        assert delete_responce.status_code == 404

        dr = delete_responce.json()

        assert dr["message"] == "Курьера с таким id нет."

