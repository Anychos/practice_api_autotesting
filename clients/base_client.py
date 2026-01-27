from typing import Any

import allure
from httpx import Client, URL, Response


class BaseAPIClient:
    """
    Базовый API клиент

    Описывает все используемые в проекте HTTP методы
    """

    def __init__(self, client: Client):
        self.client = client

    @allure.step("Отправка GET запроса на {url}")
    def get(self,
            *,
            url: str | URL,
            query_path: str | None = None
            ) -> Response:
        """
        Отправляет GET запрос

        :param url: URL ресурса
        :param query_path: Параметры запроса
        :return: Ответ сервера
        """

        return self.client.get(url=url, params=query_path)

    @allure.step("Отправка POST запроса на {url}")
    def post(self,
             *,
             url: str | URL,
             json: Any
             ) -> Response:
        """
        Отправляет POST запрос

        :param url: URL ресурса
        :param json: Данные запроса в формате JSON
        :return: Ответ сервера
        """

        return self.client.post(url=url, json=json)

    @allure.step("Отправка PUT запроса на {url}")
    def put(self,
            *,
            url: str | URL,
            json: Any
            ) -> Response:
        """
        Отправляет PUT запрос

        :param url: URL ресурса
        :param json: Данные запроса в формате JSON
        :return: Ответ сервера
        """

        return self.client.put(url=url, json=json)

    @allure.step("Отправка PATCH запроса на {url}")
    def patch(self,
            *,
            url: str | URL,
            json: Any
            ) -> Response:
        """
        Отправляет PATCH запрос

        :param url: URL ресурса
        :param json: Данные запроса в формате JSON
        :return: Ответ сервера
        """

        return self.client.patch(url=url, json=json)

    @allure.step("Отправка DELETE запроса на {url}")
    def delete(self,
               *,
               url: str | URL,
               query_path: str | None = None
               ) -> Response:
        """
        Отправляет DELETE запрос

        :param url: URL ресурса
        :param query_path: Параметры запроса
        :return: Ответ сервера
        """

        return self.client.delete(url=url, params=query_path)
