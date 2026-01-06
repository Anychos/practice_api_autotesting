from pydantic import BaseModel, Field

from tools.data_generator import fake_ru


class ProductSchema(BaseModel):
    name: str = Field(default_factory=fake_ru.object_name)
    description: str = Field(default_factory=fake_ru.description)
    price: float = Field(default_factory=fake_ru.price)
    is_available: bool = Field(default_factory=fake_ru.availability)
    image_url: str = Field(default_factory=fake_ru.image_url)

class CreateProductRequestSchema(ProductSchema):
    pass

class CreateProductResponseSchema(ProductSchema):
    id: int

class UpdateProductRequestSchema(ProductSchema):
    pass

class UpdateProductResponseSchema(ProductSchema):
    id: int

class GetProductResponseSchema(ProductSchema):
    id: int

class DeleteProductResponseSchema(BaseModel):
    message: str
