import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.authentication.schemas import LoginRequestSchema, LoginResponseSchema, RegistrationRequestSchema, \
    RegistrationResponseSchema
from clients.base_client import BaseAPIClient
from clients.public_builder import public_client_builder
from tools.routes import Routes


class AuthenticationAPIClient(BaseAPIClient):
    """
    Клиент для работы с API аутентификации
    """

    @tracker.track_coverage_httpx(Routes.LOGIN)
    @allure.step("Отправка запроса на логин пользователя")
    def login_api(self,
                  *,
                  request: LoginRequestSchema
                  ) -> Response:
        """
        Отправляет запрос на логин пользователя

        :param request: Данные пользователя для логина
        :return: Ответ сервера с данными пользователя и токеном
        """

        return self.post(url=Routes.LOGIN, json=request.model_dump())

    def login(self,
              *,
              request: LoginRequestSchema
              ) -> LoginResponseSchema:
        response = self.login_api(request=request)
        return LoginResponseSchema.model_validate_json(response.text)

    @tracker.track_coverage_httpx(Routes.REGISTRATION)
    @allure.step("Отправка запроса на регистрацию пользователя")
    def registration_api(self,
                         *,
                         request: RegistrationRequestSchema
                         ) -> Response:
        """
        Отправляет запрос на регистрацию пользователя

        :param request: Данные пользователя для регистрации
        :return: Ответ сервера с данными пользователя и токеном
        """

        return self.post(url=Routes.REGISTRATION, json=request.model_dump())

    def registration(self,
              *,
              request: RegistrationRequestSchema
              ) -> RegistrationResponseSchema:
        response = self.registration_api(request=request)
        return RegistrationResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationAPIClient:
    """
    Создает публичный HTTP клиент для доступа к API аутентификации

    :return: Публичный HTTP клиент
    """

    return AuthenticationAPIClient(client=public_client_builder())
