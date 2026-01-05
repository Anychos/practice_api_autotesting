from pydantic import BaseModel, Field

from clients.products.schemas import CreateProductResponseSchema


class CreateCartRequestSchema(BaseModel):
    product_id: int
    quantity: int = Field(default=1)
    user_id: int

class CreateCartResponseSchema(CreateCartRequestSchema):
    id: int
    product: CreateProductResponseSchema

class GetCartResponseSchema(CreateCartResponseSchema):
    pass

class UpdateCartRequestSchema(BaseModel):
    product_id: int
    quantity: int

class UpdateCartResponseSchema(CreateCartResponseSchema):
    pass
