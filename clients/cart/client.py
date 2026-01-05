from httpx import Response
import allure

from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.carts.schemas import CreateCartRequestSchema, CreateCartResponseSchema, UpdateCartRequestSchema
from clients.private_builder import get_private_client
from clients.public_builder import get_public_client
from tools.routes import Routes


class CartAPIClient(BaseAPIClient):
    @allure.step("Отправка запроса на создание корзины")
    def create_cart_api(self, request: CreateCartRequestSchema) -> Response:
        return self.post(url=Routes.CARTS, json=request.model_dump())

    def create_cart(self, request: CreateCartRequestSchema) -> CreateCartResponseSchema:
        response = self.create_cart_api(request)
        return CreateCartResponseSchema.model_validate_json(response.text)

    @allure.step("Отправка запроса на получение корзины")
    def get_cart_api(self, cart_id: int) -> Response:
        return self.get(url=f"{Routes.CARTS}/{cart_id}")

    @allure.step("Отправка запроса на получение корзин пользователя")
    def get_user_carts_api(self, user_id: int) -> Response:
        return self.get(url=f"{Routes.CARTS}/user/{user_id}")

    @allure.step("Отправка запроса на обновление корзины")
    def update_cart_api(self, cart_id: int, request: UpdateCartRequestSchema) -> Response:
        return self.put(url=f"{Routes.CARTS}/{cart_id}", json=request.model_dump())

    @allure.step("Отправка запроса на удаление корзины")
    def delete_cart_api(self, cart_id: int) -> Response:
        return self.delete(url=f"{Routes.CARTS}/{cart_id}")

def get_public_cart_client() -> CartAPIClient:
    return CartAPIClient(client=get_public_client())

def get_private_cart_client(user: LoginRequestSchema) -> CartAPIClient:
    return CartAPIClient(client=get_private_client(user))
