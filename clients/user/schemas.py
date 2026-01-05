from pydantic import BaseModel, Field

from tools.data_generator import fake


class BaseUserSchema(BaseModel):
    email: str = Field(default_factory=fake.email)
    name: str = Field(default_factory=fake.name)
    phone: str = Field(default_factory=fake.phone_number)

class FullUserSchema(BaseUserSchema):
    is_admin: bool = Field(default=False)

class CreateUserRequestSchema(FullUserSchema):
    password: str = Field(default_factory=fake.password)

class CreateUserResponseSchema(FullUserSchema):
    id: int

class GetUserResponseSchema(CreateUserResponseSchema):
    pass

class UpdateUserRequestSchema(BaseUserSchema):
    password: str = Field(default_factory=fake.password)

class UpdateUserResponseSchema(CreateUserResponseSchema):
    pass
