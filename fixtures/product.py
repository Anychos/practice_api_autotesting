from typing import Callable

import pytest
from pydantic import BaseModel

from clients.product.client import ProductAPIClient, get_public_product_client, get_private_product_client
from clients.product.schemas import CreateProductRequestSchema, CreateProductResponseSchema, \
    FullUpdateProductRequestSchema, UpdateProductResponseSchema
from fixtures.user import UserFixture


class CreateProductFixture(BaseModel):
    """
    Хранит данные о созданном товаре
    """

    request: CreateProductRequestSchema
    response: CreateProductResponseSchema

    @property
    def product_id(self) -> int:
        return self.response.id


class UpdateProductFixture(BaseModel):
    """
    Хранит данные об обновленном товаре
    """

    request: FullUpdateProductRequestSchema
    response: UpdateProductResponseSchema

    @property
    def product_id(self) -> int:
        return self.response.id


@pytest.fixture
def public_product_client() -> ProductAPIClient:
    """
    Возвращает готовый публичный HTTP клиент для доступа к API продукта

    :return: Публичный HTTP клиент для работы с API продукта
    """

    return get_public_product_client()

@pytest.fixture
def admin_private_product_client(admin: UserFixture) -> ProductAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа администратора к API продукта

    :param admin: Созданный администратор
    :return: Приватный HTTP клиент администратора для работы с API продукта
    """

    return get_private_product_client(user=admin.user_schema)

@pytest.fixture
def user_private_product_client(user: UserFixture) -> ProductAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа пользователя к API продукта

    :param user: Созданный пользователь
    :return: Приватный HTTP клиент пользователя для работы с API продукта
    """

    return get_private_product_client(user=user.user_schema)


@pytest.fixture
def create_product_factory(admin_private_product_client: ProductAPIClient) -> Callable[..., CreateProductFixture]:
    """
    Возвращает фабрику для создания продукта

    :param admin_private_product_client: Приватный HTTP клиент для доступа к API продукта
    :return: Фабрика для создания продукта
    """

    def _create_product(
            *,
            is_available: bool = True,
            stock_quantity: int = 1
    ) -> CreateProductFixture:
        """
        Создает продукт с указанными параметрами

        :param is_available: Флаг доступности
        :param stock_quantity: Количество продукта
        :return: Объект ProductFixture с информацией о продукте
        """

        request = CreateProductRequestSchema(
            is_available=is_available,
            stock_quantity=stock_quantity
        )
        response = admin_private_product_client.create_product(request=request)
        return CreateProductFixture(request=request, response=response)

    return _create_product


@pytest.fixture
def create_available_product(create_product_factory: Callable[..., CreateProductFixture]) -> CreateProductFixture:
    """
    Возвращает созданный продукт

    :param create_product_factory: Фабрика для создания продукта
    :return: Объект ProductFixture с информацией о продукте
    """

    return create_product_factory()


@pytest.fixture
def update_product_factory(admin_private_product_client: ProductAPIClient) -> Callable[..., UpdateProductFixture]:
    """
    Возвращает фабрику для обновления продукта

    :param admin_private_product_client: Приватный HTTP клиент для доступа к API продукта
    :return: Фабрика для обновления продукта
    """

    def _update_product(
            *,
            product_id: int,
            description: str = "product description",
            image_url: str = "https://example.com/image.jpg",
            is_available: bool = True,
            name: str = "product name",
            price: float = 1000,
            stock_quantity: int = 1
    ) -> UpdateProductFixture:
        """
        Обновляет продукт с указанными параметрами

        :param product_id: Идентификатор продукта
        :param is_available: Флаг доступности
        :param stock_quantity: Количество продукта
        :return: Объект ProductFixture с информацией об обновленном продукте
        """

        request = FullUpdateProductRequestSchema(
            description=description,
            image_url=image_url,
            name=name,
            price=price,
            is_available=is_available,
            stock_quantity=stock_quantity
        )
        response = admin_private_product_client.full_update_product(product_id=product_id, request=request)
        return UpdateProductFixture(request=request, response=response)

    return _update_product
