from pydantic import BaseModel

from clients.users.user_schema import CreateUserResponseSchema


class LoginRequestSchema(BaseModel):
    email: str
    password: str

class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user: CreateUserResponseSchema
