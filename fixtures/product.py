import pytest
from pydantic import BaseModel

from clients.product.client import ProductAPIClient, get_public_product_client, get_private_product_client
from clients.product.schemas import CreateProductRequestSchema, CreateProductResponseSchema
from fixtures.user import UserFixture


class ProductFixture(BaseModel):
    """
    Модель хранит данные о созданном товаре
    """
    request: CreateProductRequestSchema
    response: CreateProductResponseSchema

    @property
    def product_id(self) -> int:
        return self.response.id

@pytest.fixture
def public_product_client() -> ProductAPIClient:
    """
    Возвращает готовый публичный HTTP клиент для доступа к API продуктов

    :return: HTTP клиент
    """
    return get_public_product_client()

@pytest.fixture
def admin_private_product_client(admin: UserFixture) -> ProductAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа администратора к API продуктов

    :param admin: Администратор
    :return: HTTP клиент
    """
    return get_private_product_client(user=admin.user_schema)

@pytest.fixture
def user_private_product_client(user: UserFixture) -> ProductAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа пользователя к API продуктов

    :param user: Пользователь
    :return: HTTP клиент
    """
    return get_private_product_client(user=user.user_schema)

@pytest.fixture
def create_product(admin_private_product_client: ProductAPIClient) -> ProductFixture:
    """
    Создает продукт

    :param admin_private_product_client: Приватный HTTP клиент для доступа к API продуктов
    :return: Информация о созданном продукте
    """
    request = CreateProductRequestSchema()
    response = admin_private_product_client.create_product(request)
    return ProductFixture(request=request, response=response)
