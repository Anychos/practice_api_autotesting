import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.authentication.schemas import LoginRequestSchema, LoginResponseSchema
from clients.base_client import BaseAPIClient
from clients.public_builder import get_public_client
from tools.routes import Routes


class AuthenticationAPIClient(BaseAPIClient):
    """
    Клиент для работы с API аутентификации
    """
    @allure.step("Отправка запроса на логин пользователя")
    @tracker.track_coverage_httpx(Routes.LOGIN)
    def login_api(self, request: LoginRequestSchema) -> Response:
        return self.post(url=Routes.LOGIN, json=request.model_dump())

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)

def get_login_client() -> AuthenticationAPIClient:
    """
    Создает публичный HTTP клиент для доступа к API аутентификации

    :return: Публичный HTTP клиент
    """
    return AuthenticationAPIClient(client=get_public_client())
