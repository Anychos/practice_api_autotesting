import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema, UpdateCartItemRequestSchema
from clients.private_builder import private_user_client_builder
from clients.public_builder import get_public_client
from tools.routes import Routes


class CartAPIClient(BaseAPIClient):
    """
    Клиент для работы с API корзины
    """

    @tracker.track_coverage_httpx(f"{Routes.CARTS}/items")
    @allure.step("Отправка запроса на создание корзины")
    def add_item_cart_api(self,
                          *,
                          request: AddItemCartRequestSchema
                          ) -> Response:
        """
        Отправляет запрос на добавление продукта в корзину

        :param request: Данные для добавления продукта
        :return: Ответ сервера с данными добавленного продукта
        """

        return self.post(url=f"{Routes.CARTS}/items", json=request.model_dump())

    def add_item_cart(self,
                      *,
                      request: AddItemCartRequestSchema
                      ) -> AddItemCartResponseSchema:
        response = self.add_item_cart_api(request=request)
        return AddItemCartResponseSchema.model_validate_json(response.text)

    @tracker.track_coverage_httpx(Routes.CARTS)
    @allure.step("Отправка запроса на получение корзины")
    def get_cart_api(self) -> Response:
        """
        Отправляет запрос на получение корзины

        :return: Ответ сервера с данными корзины
        """

        return self.get(url=Routes.CARTS)

    @tracker.track_coverage_httpx(f"{Routes.CARTS}/items/" + "{product_id}")
    @allure.step("Отправка запроса на обновление корзины")
    def update_cart_item_api(self,
                             *,
                             item_id: int,
                             request: UpdateCartItemRequestSchema
                             ) -> Response:
        """
        Отправляет запрос на обновление продукта в корзине

        :param item_id: ID продукта в корзине
        :param request: Данные для обновления продукта
        :return: Ответ сервера с обновленным продуктом
        """

        return self.put(url=f"{Routes.CARTS}/items/{item_id}", json=request.model_dump())

    @tracker.track_coverage_httpx(f"{Routes.CARTS}/items/" + "{product_id}")
    @allure.step("Отправка запроса на удаление продукта из корзины")
    def remove_item_cart_api(self,
                             *,
                             item_id: int
                             ) -> Response:
        """
        Отправляет запрос на удаление продукта из корзины

        :param item_id: ID продукта в корзине
        :return: Ответ сервера с сообщением об удалении продукта из корзины
        """

        return self.delete(url=f"{Routes.CARTS}/items/{item_id}")

    @tracker.track_coverage_httpx(Routes.CARTS)
    @allure.step("Отправка запроса на удаление корзины")
    def delete_cart_api(self) -> Response:
        """
        Отправляет запрос на очистку корзины

        :return: Ответ сервера с сообщением об очистке корзины
        """

        return self.delete(url=Routes.CARTS)


def get_public_cart_client() -> CartAPIClient:
    """
    Создает публичный HTTP клиент для доступа к API корзины

    :return: Публичный HTTP клиент
    """

    return CartAPIClient(client=get_public_client())

def get_private_cart_client(
        *,
        user: LoginRequestSchema
) -> CartAPIClient:
    """
    Создает приватный HTTP клиент для доступа к API корзины

    :param user: Данные пользователя для авторизации
    :return: Приватный HTTP клиент
    """

    return CartAPIClient(client=private_user_client_builder(user=user))
