from typing import Any

import allure
from httpx import Client, URL


class BaseAPIClient:
    """
    Базовый класс API клиента

    Описывает все используемые HTTP методы
    """
    def __init__(self, client: Client):
        self.client = client

    @allure.step("Отправка GET запроса на {url}")
    def get(self, url: str | URL, query_path: str | None = None):
        return self.client.get(url, params=query_path)

    @allure.step("Отправка POST запроса на {url}")
    def post(self, url: str | URL, json: Any):
        return self.client.post(url, json=json)

    @allure.step("Отправка PUT запроса на {url}")
    def put(self, url: str | URL, json: Any):
        return self.client.put(url, json=json)

    @allure.step("Отправка DELETE запроса на {url}")
    def delete(self, url: str | URL, query_path: str | None = None):
        return self.client.delete(url, params=query_path)
