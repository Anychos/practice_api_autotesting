import allure
from httpx import Response

from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema, UpdateCartItemRequestSchema
from clients.private_builder import get_private_client
from clients.public_builder import get_public_client
from tools.routes import Routes


class CartAPIClient(BaseAPIClient):
    @allure.step("Отправка запроса на создание корзины")
    def add_item_cart_api(self, request: AddItemCartRequestSchema) -> Response:
        return self.post(url=f"{Routes.CARTS}/items", json=request.model_dump())

    def add_item_cart(self, request: AddItemCartRequestSchema) -> AddItemCartResponseSchema:
        response = self.add_item_cart_api(request)
        return AddItemCartResponseSchema.model_validate_json(response.text)

    @allure.step("Отправка запроса на получение корзины")
    def get_cart_api(self) -> Response:
        return self.get(url=Routes.CARTS)

    @allure.step("Отправка запроса на обновление корзины")
    def update_cart_item_api(self, item_id: int, request: UpdateCartItemRequestSchema) -> Response:
        return self.put(url=f"{Routes.CARTS}/items/{item_id}", json=request.model_dump())

    @allure.step("Отправка запроса на удаление продукта из корзины")
    def remove_item_cart_api(self, item_id: int) -> Response:
        return self.delete(url=f"{Routes.CARTS}/items/{item_id}")

    @allure.step("Отправка запроса на удаление корзины")
    def delete_cart_api(self) -> Response:
        return self.delete(url=Routes.CARTS)

def get_public_cart_client() -> CartAPIClient:
    return CartAPIClient(client=get_public_client())

def get_private_cart_client(user: LoginRequestSchema) -> CartAPIClient:
    return CartAPIClient(client=get_private_client(user))
