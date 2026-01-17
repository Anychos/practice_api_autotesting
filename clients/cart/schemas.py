from typing import List

from pydantic import BaseModel, Field


class ItemInCartSchema(BaseModel):
    product_id: int
    quantity: int
    product_name: str
    product_price: int | float
    product_image_url: str
    is_available: bool
    has_enough_stock: bool
    available_quantity: int


class AddItemCartRequestSchema(BaseModel):
    product_id: int
    quantity: int = Field(default=1)


class AddItemCartResponseSchema(AddItemCartRequestSchema):
    cart_id: int


class GetCartResponseSchema(BaseModel):
    id: int
    user_id: int
    total_quantity: int
    total_price: int
    items: List[ItemInCartSchema]


class UpdateCartItemRequestSchema(BaseModel):
    quantity: int = Field(default=1)


class UpdateCartItemResponseSchema(AddItemCartResponseSchema):
    pass


class DeleteCartItemResponseSchema(BaseModel):
    message: str


class DeleteCartResponseSchema(DeleteCartItemResponseSchema):
    pass

