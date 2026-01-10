import allure
from httpx import Response

from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.private_builder import get_private_client
from clients.public_builder import get_public_client
from clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserRequestSchema
from tools.routes import Routes
from clients.api_coverage import tracker


class UserAPIClient(BaseAPIClient):
    @allure.step("Отправка запроса на создание пользователя")
    @tracker.track_coverage_httpx(Routes.USERS)
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        return self.post(url=Routes.USERS, json=request.model_dump())

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)

    @allure.step("Отправка запроса на получение пользователя")
    @tracker.track_coverage_httpx(f"{Routes.USERS}/" + "{user_id}")
    def get_user_api(self, user_id: int) -> Response:
        return self.get(url=f"{Routes.USERS}/{user_id}")

    @allure.step("Отправка запроса на обновление пользователя")
    @tracker.track_coverage_httpx(f"{Routes.USERS}/" + "{user_id}")
    def update_user_api(self, user_id: int, request: UpdateUserRequestSchema) -> Response:
        return self.put(url=f"{Routes.USERS}/{user_id}", json=request.model_dump())

    @allure.step("Отправка запроса на удаление пользователя")
    @tracker.track_coverage_httpx(f"{Routes.USERS}/" + "{user_id}")
    def delete_user_api(self, user_id: int) -> Response:
        return self.delete(url=f"{Routes.USERS}/{user_id}")

def get_public_user_client() -> UserAPIClient:
    return UserAPIClient(client=get_public_client())

def get_private_user_client(user: LoginRequestSchema) -> UserAPIClient:
    return UserAPIClient(client=get_private_client(user))
