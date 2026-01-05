import pytest
from pydantic import BaseModel

from clients.products.client import ProductAPIClient, get_public_product_client, get_private_product_client
from clients.products.schemas import CreateProductRequestSchema, CreateProductResponseSchema
from fixtures.users import UserFixture


class ProductFixture(BaseModel):
    request: CreateProductRequestSchema
    response: CreateProductResponseSchema

    @property
    def product_id(self) -> int:
        return self.response.id

@pytest.fixture
def public_product_client() -> ProductAPIClient:
    return get_public_product_client()

@pytest.fixture
def admin_private_product_client(admin: UserFixture) -> ProductAPIClient:
    return get_private_product_client(user=admin.user)

@pytest.fixture
def user_private_product_client(user: UserFixture) -> ProductAPIClient:
    return get_private_product_client(user=user.user)

@pytest.fixture
def create_product(private_product_client: ProductAPIClient) -> ProductFixture:
    request = CreateProductRequestSchema()
    response = private_product_client.create_product(request)
    return ProductFixture(request=request, response=response)
