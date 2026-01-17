from typing import Callable

import pytest
from pydantic import BaseModel

from clients.cart.client import CartAPIClient, get_public_cart_client, get_private_cart_client
from clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema
from fixtures.product import ProductFixture
from fixtures.user import UserFixture


class CartFixture(BaseModel):
    """
    Хранит данные о созданной корзине
    """

    request: AddItemCartRequestSchema
    response: AddItemCartResponseSchema

    @property
    def cart_id(self) -> int:
        return self.response.cart_id

    @property
    def item_id(self) -> int:
        return self.response.product_id


@pytest.fixture
def public_cart_client() -> CartAPIClient:
    """
    Возвращает готовый публичный HTTP клиент для доступа к API корзины

    :return: Публичный HTTP клиент для работы с API корзины
    """

    return get_public_cart_client()

@pytest.fixture
def private_cart_client(create_user_factory: Callable[..., UserFixture]) -> CartAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа к API корзины

    :param create_user_factory: Фабрика для создания пользователя
    :return: Приватный HTTP клиент для работы с API корзины
    """

    user = create_user_factory()
    return get_private_cart_client(user=user.user_schema)


@pytest.fixture
def create_cart_factory(
        private_cart_client: CartAPIClient,
        create_product_factory: Callable[..., ProductFixture]
) -> Callable[..., CartFixture]:
    """
    Возвращает фабрику для создания корзины с продуктом

    :param private_cart_client: Приватный HTTP клиент для доступа к API корзины
    :param create_product_factory: Фабрика для создания продукта
    :return: Фабрика для создания корзины с продуктом
    """

    def _create_cart(
            *,
            is_available: bool = True,
            stock_quantity: int = 1
    ) -> CartFixture:
        """
        Создает корзину с продуктом с указанными параметрами

        :param is_available: Флаг доступности продукта
        :param stock_quantity: Количество продукта на складе
        :return: Объект CartFixture с информацией о корзине
        """

        product = create_product_factory(is_available=is_available,
                                         stock_quantity=stock_quantity)
        request = AddItemCartRequestSchema(product_id=product.product_id)
        response = private_cart_client.add_item_cart(request=request)
        return CartFixture(request=request, response=response)

    return _create_cart
