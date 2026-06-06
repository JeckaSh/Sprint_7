import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests
import allure
from utils.data import generate_random_string, generate_random_number


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

    @allure.step("Создаём курьера со случайными поля login, password, firstName")
    def create_courier(self):
        """
        Создание random данных для login, password и firstName полей
        """
        login = generate_random_string(10)
        password = generate_random_string(10)
        firstName = generate_random_string(10)

        return {"login": login, "password": password, "firstName": firstName}
