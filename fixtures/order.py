from typing import Callable

import pytest
from pydantic import BaseModel

from clients.order.client import OrderAPIClient, get_public_order_client, get_private_order_client
from clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema
from fixtures.cart import CartFixture
from fixtures.user import UserFixture


class OrderFixture(BaseModel):
    """
    Хранит данные о созданном заказе
    """

    request: CreateOrderRequestSchema
    response: CreateOrderResponseSchema

    @property
    def order_id(self) -> int:
        return self.response.id


@pytest.fixture
def public_order_client() -> OrderAPIClient:
    """
    Возвращает готовый публичный HTTP клиент для доступа к API заказа

    :return: Публичный HTTP клиент для работы с API заказа
    """

    return get_public_order_client()

@pytest.fixture
def private_order_client(create_user_factory: Callable[..., UserFixture]) -> OrderAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа к API заказов

    :param create_user_factory: Фабрика для создания пользователя
    :return: Приватный HTTP клиент для работы с API заказа
    """

    user = create_user_factory()
    return get_private_order_client(user=user.user_schema)


@pytest.fixture
def create_order(private_order_client: OrderAPIClient, create_cart: CartFixture) -> OrderFixture:
    """
    Создает заказ

    :param private_order_client: Приватный HTTP клиент для доступа к API заказов
    :param create_cart: Созданная корзина
    :return: Информация о созданном заказе
    """

    request = CreateOrderRequestSchema(cart_id=create_cart.cart_id)
    response = private_order_client.create_order(request)
    return OrderFixture(request=request, response=response)
