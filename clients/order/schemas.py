from pydantic import BaseModel

from clients.carts.schemas import CreateCartResponseSchema


class CreateOrderRequestSchema(BaseModel):
    cart_id: int

class CreateOrderResponseSchema(CreateOrderRequestSchema):
    id: int
    created_at: str
    user_id: int
    cart: CreateCartResponseSchema

class GetOrderResponseSchema(CreateOrderResponseSchema):
    pass
