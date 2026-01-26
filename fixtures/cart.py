import pytest
from pydantic import BaseModel

from clients.cart.client import CartAPIClient, get_public_cart_client, get_private_cart_client
from clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema
from fixtures.product import CreateProductFixture
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
def private_cart_client(user: UserFixture) -> CartAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа к API корзины

    :param user: Созданный пользователь
    :return: Приватный HTTP клиент для работы с API корзины
    """

    return get_private_cart_client(user=user.user_schema)


@pytest.fixture
def create_cart(
        private_cart_client: CartAPIClient,
        create_available_product: CreateProductFixture
) -> CartFixture:
    """
    Создает корзину с продуктом

    :param private_cart_client: Приватный HTTP клиент для доступа к API корзины
    :param create_available_product: Созданный продукт
    :return: Объект CartFixture с информацией о корзине
    """

    request = AddItemCartRequestSchema(product_id=create_available_product.product_id)
    response = private_cart_client.add_item_cart(request=request)
    return CartFixture(request=request, response=response)


@pytest.fixture
def empty_cart(
    private_cart_client: CartAPIClient,
    create_cart: CartFixture
) -> CartFixture:
    """
    Создает корзину и очищает ее

    :param private_cart_client: Приватный HTTP клиент для доступа к API корзины
    :param create_cart: Созданная корзина
    :return: Объект CartFixture с информацией о корзине
    """
    private_cart_client.delete_cart_api()
    return create_cart

