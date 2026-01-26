from pydantic import BaseModel, EmailStr, Field

from clients.user.schemas import CreateUserResponseSchema
from tools.data_generator import fake_ru


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user: CreateUserResponseSchema


class RegistrationRequestSchema(BaseModel):
    email: EmailStr = Field(default_factory=fake_ru.email)
    password: str = Field(default_factory=fake_ru.password)
    name: str = Field(default_factory=fake_ru.first_name)
    phone: str = Field(default_factory=fake_ru.phone)


class RegistrationResponseSchema(LoginResponseSchema):
    pass
