from typing import List

from pydantic import BaseModel


class CreateOrderRequestSchema(BaseModel):
    cart_id: int


class CreateOrderResponseSchema(BaseModel):
    id: int
    cart_id: int
    created_at: str
    user_id: int


class GetOrderResponseSchema(CreateOrderResponseSchema):
    pass


GetOrdersResponseSchema = List[GetOrderResponseSchema]
