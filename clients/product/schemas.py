from typing import Optional, List

from pydantic import BaseModel, Field

from tools.data_generator import fake_ru


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool
    image_url: str
    stock_quantity: int


class CreateProductRequestSchema(ProductSchema):
    name: str = Field(default_factory=fake_ru.object_name)
    description: str = Field(default_factory=fake_ru.description)
    price: int | float = Field(default_factory=fake_ru.price)
    is_available: bool = Field(default_factory=fake_ru.availability)
    image_url: str = Field(default_factory=fake_ru.image_url)
    stock_quantity: int = Field(default_factory=fake_ru.quantity)


class CreateProductResponseSchema(ProductSchema):
    id: int


class FullUpdateProductRequestSchema(CreateProductRequestSchema):
    pass


class PartialUpdateProductRequestSchema(ProductSchema):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[int | float] = Field(default=None)
    is_available: Optional[bool] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    stock_quantity: Optional[int] = Field(default=None)


class UpdateProductResponseSchema(CreateProductResponseSchema):
    pass


class GetProductResponseSchema(CreateProductResponseSchema):
    pass


GetProductsResponseSchema = List[GetProductResponseSchema]


class DeleteProductResponseSchema(BaseModel):
    message: str
