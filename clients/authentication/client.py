from httpx import Response

from authentication.authentication_shema import LoginRequestSchema, LoginResponseSchema
from clients.base_client import BaseAPIClient
from clients.public_builder import get_public_client
from tools.routes import Routes


class AuthenticationAPIClient(BaseAPIClient):
    def login_api(self, request: LoginRequestSchema) -> Response:
        return self.post(url=Routes.LOGIN, json=request.model_dump())

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)

def get_public_login_client() -> AuthenticationAPIClient:
    return AuthenticationAPIClient(client=get_public_client())
