from typing import List

from pydantic import BaseModel, Field


class AddItemCartRequestSchema(BaseModel):
    product_id: int
    quantity: int = Field(default=1)

class AddItemCartResponseSchema(AddItemCartRequestSchema):
    cart_id: int

class GetCartResponseSchema(BaseModel):
    id: int
    user_id: int
    total_quantity: int
    items: List[AddItemCartRequestSchema]

class UpdateCartItemRequestSchema(BaseModel):
    quantity: int = Field(default=2)

class UpdateCartItemResponseSchema(AddItemCartResponseSchema):
    pass

class DeleteCartItemResponseSchema(BaseModel):
    message: str

class DeleteCartResponseSchema(DeleteCartItemResponseSchema):
    pass

