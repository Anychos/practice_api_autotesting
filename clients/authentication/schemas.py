from pydantic import BaseModel, EmailStr

from clients.user.schemas import CreateUserResponseSchema


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user: CreateUserResponseSchema
