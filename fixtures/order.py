import pytest
from pydantic import BaseModel

from clients.order.client import OrderAPIClient, get_public_order_client, get_private_order_client
from clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema
from fixtures.cart import CartFixture
from fixtures.user import UserFixture


class OrderFixture(BaseModel):
    request: CreateOrderRequestSchema
    response: CreateOrderResponseSchema

    @property
    def order_id(self) -> int:
        return self.response.id

@pytest.fixture
def public_order_client() -> OrderAPIClient:
    return get_public_order_client()

@pytest.fixture
def private_order_client(user: UserFixture) -> OrderAPIClient:
    return get_private_order_client(user=user.user_schema)

@pytest.fixture
def create_order(private_order_client: OrderAPIClient, create_cart: CartFixture) -> OrderFixture:
    request = CreateOrderRequestSchema(cart_id=create_cart.cart_id)
    response = private_order_client.create_order(request)
    return OrderFixture(request=request, response=response)
