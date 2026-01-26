from pydantic import BaseModel, Field

from tools.data_generator import fake_ru


class UserSchema(BaseModel):
    email: str = Field(default_factory=fake_ru.email)
    name: str = Field(default_factory=fake_ru.first_name)
    phone: str = Field(default_factory=fake_ru.phone)


class CreateUserRequestSchema(UserSchema):
    password: str = Field(default_factory=fake_ru.password)
    is_admin: bool = Field(default=True)


class CreateUserResponseSchema(UserSchema):
    id: int
    is_admin: bool


class GetUserResponseSchema(CreateUserResponseSchema):
    pass


class GetUserMeResponseSchema(CreateUserResponseSchema):
    pass


class UpdateUserRequestSchema(UserSchema):
    pass


class UpdateUserResponseSchema(CreateUserResponseSchema):
    pass


class UpdatePasswordRequestSchema(BaseModel):
    current_password: str
    new_password: str


class UpdatePasswordResponseSchema(CreateUserResponseSchema):
    pass


class DeleteUserResponseSchema(BaseModel):
    message: str
