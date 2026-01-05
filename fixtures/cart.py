import pytest
from pydantic import BaseModel

from clients.carts.client import CartAPIClient, get_public_cart_client, get_private_cart_client
from clients.carts.schemas import CreateCartRequestSchema, CreateCartResponseSchema
from clients.products.client import ProductAPIClient
from fixtures.users import UserFixture


class CartFixture(BaseModel):
    request: CreateCartRequestSchema
    response: CreateCartResponseSchema

    @property
    def cart_id(self) -> int:
        return self.response.id

@pytest.fixture
def public_cart_client() -> CartAPIClient:
    return get_public_cart_client()

@pytest.fixture
def private_cart_client(user: UserFixture) -> CartAPIClient:
    return get_private_cart_client(user=user.user)

@pytest.fixture
def create_cart(public_cart_client: CartAPIClient, user, create_product) -> CartFixture:
    request = CreateCartRequestSchema(product_id=create_product.product_id, user_id=user.user_id)
    response = public_cart_client.create_cart(request)
    return CartFixture(request=request, response=response)
