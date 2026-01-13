import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema
from clients.private_builder import get_private_client
from clients.public_builder import get_public_client
from tools.routes import Routes


class OrderAPIClient(BaseAPIClient):
    """
    Клиент для работы с API заказов
    """
    @allure.step("Отправка запроса на создание заказа")
    @tracker.track_coverage_httpx(Routes.ORDERS)
    def create_order_api(self, request: CreateOrderRequestSchema) -> Response:
        return self.post(url=Routes.ORDERS, json=request.model_dump())

    def create_order(self, request: CreateOrderRequestSchema) -> CreateOrderResponseSchema:
        response = self.create_order_api(request)
        return CreateOrderResponseSchema.model_validate_json(response.text)

    @allure.step("Отправка запроса на получение заказа")
    @tracker.track_coverage_httpx(f"{Routes.ORDERS}/" + "{order_id}")
    def get_order_api(self, order_id: int) -> Response:
        return self.get(url=f"{Routes.ORDERS}/{order_id}")

    @allure.step("Отправка запроса на получение заказов пользователя")
    @tracker.track_coverage_httpx(Routes.ORDERS)
    def get_orders_api(self) -> Response:
        return self.get(url=Routes.ORDERS)

def get_public_order_client() -> OrderAPIClient:
    """
    Создает публичный HTTP клиент для доступа к API заказов

    :return: Публичный HTTP клиент
    """
    return OrderAPIClient(client=get_public_client())

def get_private_order_client(user: LoginRequestSchema) -> OrderAPIClient:
    """
    Создает приватный HTTP клиент для доступа к API заказов

    :param user: Пользователь
    :return: Приватный HTTP клиент
    """
    return OrderAPIClient(client=get_private_client(user))
