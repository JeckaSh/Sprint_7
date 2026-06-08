import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests
import allure
from utils.helpers import generate_random_string
from utils.data import ApiData


class ApiClient:
    """
    Базовый API клиент для предоставления методов работы с API
    """

    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.session = requests.Session()

        if token:
            self.set_token(token)

    def set_token(self, token):
        """
        Установка токена для аутентификации
        """
        self.token = token
        self.session.headers.update({"Authorization": f"{token}"})

    def _make_request(self, method, endpoint, **kwargs):
        """
        Общий метод для создания запроса
        """
        url = f"{self.base_url}{endpoint}"
        responce = self.session.request(method, url, **kwargs)
        return responce

    @allure.step("Отправка GET запроса")
    def get(self, endpoint, params=None, headers=None):
        """
        GET запрос
        """
        return self._make_request("GET", endpoint, params=params, headers=headers)

    @allure.step("Отправка POST запроса")
    def post(self, endpoint, data=None, params=None, headers=None):
        """
        POST запрос
        """
        return self._make_request(
            "POST", endpoint, data=data, params=params, headers=headers
        )

    @allure.step("Отправка PUT запроса")
    def put(self, endpoint, data=None, params=None, headers=None):
        """
        PUT запрос
        """
        return self._make_request(
            "PUT", endpoint, data=data, params=params, headers=headers
        )

    @allure.step("Отправка PATCH запроса")
    def patch(self, endpoint, data=None, json=None, headers=None):
        """
        PATCH запрос
        """
        return self._make_request(
            "PATCH", endpoint, data=data, json=json, headers=headers
        )

    @allure.step("Отправка DELETE запроса")
    def delete(self, endpoint, headers=None):
        """
        DELETE запрос
        """
        return self._make_request("DELETE", endpoint, headers=headers)

    @allure.step("Создание курьера со случайными поля login, password, firstName")
    def create_courier(self):
        """
        Создание random данных для login, password и firstName полей
        """
        login = generate_random_string(10)
        password = generate_random_string(10)
        firstName = generate_random_string(10)

        return {"login": login, "password": password, "firstName": firstName}

    @allure.step("Удаление курьера")
    def delete_courier(self, id):
        """
        Удаление курьера по id
        """
        return self.delete(f"{ApiData.courier_endpoint}/{id}")

    @allure.step("Создание данных для создания заказа")
    def create_order(self):
        """
        Создание данных для полей заказа
        """
        return {
            "firstName": "Naruto123",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
        }

    @allure.step("Создание данных для создания заказа, передаём в [color] цвет заказа")
    def create_order_with_color(self, color):
        """
        Создание данных для полей заказа с возможностью указать цвет заказа
        """
        return {
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

    @allure.step("Отменяем заказ")
    def cancel_order(self, track):
        """
        Отмена заказа
        """
        data = {"track": track}
        return self.put(ApiData.cancel_order, data=data)
