from typing import Optional

from pydantic import BaseModel, Field

from tools.data_generator import fake_ru


class ProductSchema(BaseModel):
    name: str = Field(default_factory=fake_ru.object_name)
    description: str = Field(default_factory=fake_ru.description)
    price: int | float = Field(default_factory=fake_ru.price)
    is_available: bool = Field(default_factory=fake_ru.availability)
    image_url: str = Field(default_factory=fake_ru.image_url)
    stock_quantity: int = Field(default_factory=fake_ru.quantity)


class CreateProductRequestSchema(ProductSchema):
    pass


class CreateProductResponseSchema(ProductSchema):
    id: int


class FullUpdateProductRequestSchema(ProductSchema):
    pass


class PartialUpdateProductRequestSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[int | float] = Field(default=None)
    is_available: Optional[bool] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    stock_quantity: Optional[int] = Field(default=None)

class UpdateProductResponseSchema(ProductSchema):
    id: int


class GetProductResponseSchema(ProductSchema):
    id: int


class DeleteProductResponseSchema(BaseModel):
    message: str
