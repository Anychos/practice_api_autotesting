from pydantic import BaseModel, Field

from tools.data_generator import fake


class ProductSchema(BaseModel):
    name: str = Field(default_factory=fake.object_name)
    description: str = Field(default_factory=fake.description)
    price: float = Field(default_factory=fake.price)
    is_available: bool = Field(default_factory=fake.availability)
    image_url: str = Field(default_factory=fake.image_url)

class CreateProductRequestSchema(ProductSchema):
    pass

class CreateProductResponseSchema(CreateProductRequestSchema):
    id: int

class UpdateProductRequestSchema(ProductSchema):
    pass

class UpdateProductResponseSchema(UpdateProductRequestSchema):
    id: int

class GetProductResponseSchema(ProductSchema):
    id: int
