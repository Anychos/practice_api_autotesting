import allure
from httpx import Response

from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema
from clients.private_builder import get_private_client
from clients.public_builder import get_public_client
from tools.routes import Routes


class OrderAPIClient(BaseAPIClient):
    @allure.step("Отправка запроса на создание заказа")
    def create_order_api(self, request: CreateOrderRequestSchema) -> Response:
        return self.post(url=Routes.ORDERS, json=request.model_dump())

    def create_order(self, request: CreateOrderRequestSchema) -> CreateOrderResponseSchema:
        response = self.create_order_api(request)
        return CreateOrderResponseSchema.model_validate_json(response.text)

    @allure.step("Отправка запроса на получение заказа")
    def get_order_api(self, order_id: int) -> Response:
        return self.get(url=f"{Routes.ORDERS}/{order_id}")

    @allure.step("Отправка запроса на получение заказов пользователя")
    def get_orders_api(self, user_id: int) -> Response:
        return self.get(url=f"{Routes.ORDERS}/user/{user_id}")

def get_public_order_client() -> OrderAPIClient:
    return OrderAPIClient(client=get_public_client())

def get_private_order_client(user: LoginRequestSchema) -> OrderAPIClient:
    return OrderAPIClient(client=get_private_client(user))
