from pydantic import BaseModel


class CreateOrderRequestSchema(BaseModel):
    cart_id: int


class CreateOrderResponseSchema(CreateOrderRequestSchema):
    id: int
    created_at: str
    user_id: int


class GetOrderResponseSchema(CreateOrderResponseSchema):
    pass
