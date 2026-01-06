import pytest
from pydantic import BaseModel

from clients.cart.client import CartAPIClient, get_public_cart_client, get_private_cart_client
from clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema
from fixtures.product import ProductFixture
from fixtures.user import UserFixture


class CartFixture(BaseModel):
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
    return get_public_cart_client()

@pytest.fixture
def private_cart_client(user: UserFixture) -> CartAPIClient:
    return get_private_cart_client(user=user.user_schema)

@pytest.fixture
def create_cart(private_cart_client: CartAPIClient, user: UserFixture, create_product: ProductFixture) -> CartFixture:
    request = AddItemCartRequestSchema(product_id=create_product.product_id)
    response = private_cart_client.add_item_cart(request)
    return CartFixture(request=request, response=response)
