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


class UpdateProductRequestSchema(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | float | None = Field(default=None)
    is_available: bool | None = Field(default=None)
    image_url: str | None = Field(default=None)
    stock_quantity: int | None = Field(default=None)


class UpdateProductResponseSchema(ProductSchema):
    id: int


class GetProductResponseSchema(ProductSchema):
    id: int


class DeleteProductResponseSchema(BaseModel):
    message: str
