import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.private_builder import private_user_client_builder, private_admin_client_builder
from clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserRequestSchema, \
    UpdatePasswordRequestSchema
from config import settings
from tools.routes import Routes


class UserAPIClient(BaseAPIClient):
    """
    Клиент для работы с API пользователя
    """

    @tracker.track_coverage_httpx(Routes.USERS)
    @allure.step("Отправка запроса на создание пользователя")
    def create_user_api(self,
                        *,
                        request: CreateUserRequestSchema
                        ) -> Response:
        """
        Отправляет запрос на создание пользователя

        :param request: Данные для создания пользователя
        :return: Ответ сервера с данными созданного пользователя
        """

        return self.post(url=Routes.USERS, json=request.model_dump())

    def create_user(self,
                    *,
                    request: CreateUserRequestSchema
                    ) -> CreateUserResponseSchema:
        response = self.create_user_api(request=request)
        return CreateUserResponseSchema.model_validate_json(response.text)

    @tracker.track_coverage_httpx(f"{Routes.USERS}/" + "{user_id}")
    @allure.step("Отправка запроса на получение пользователя по id")
    def get_user_api(self,
                     *,
                     user_id: int
                     ) -> Response:
        """
        Отправляет запрос на получение пользователя

        :param user_id: Идентификатор пользователя
        :return: Ответ сервера с данными пользователя
        """

        return self.get(url=f"{Routes.USERS}/{user_id}")

    @tracker.track_coverage_httpx("/user/me")
    @allure.step("Отправка запроса на получение текущего пользователя")
    def get_user_me_api(self) -> Response:
        """
        Отправляет запрос на получение текущего пользователя

        :return: Ответ сервера с данными пользователя
        """

        return self.get(url="/user/me")

    @tracker.track_coverage_httpx(f"{Routes.USERS}/" + "{user_id}")
    @allure.step("Отправка запроса на обновление данных пользователя")
    def update_user_api(self,
                        *,
                        user_id: int,
                        request: UpdateUserRequestSchema
                        ) -> Response:
        """
        Отправляет запрос на обновление пользователя

        :param user_id: Идентификатор пользователя
        :param request: Данные для обновления пользователя
        :return: Ответ сервера с данными обновленного пользователя
        """

        return self.put(url=f"{Routes.USERS}/{user_id}", json=request.model_dump())

    @tracker.track_coverage_httpx(f"{Routes.USERS}/" + "{user_id}/password")
    @allure.step("Отправка запроса на обновление пароля пользователя")
    def update_password_api(self,
                            *,
                            user_id: int,
                            request: UpdatePasswordRequestSchema
                            ) -> Response:
        """
        Отправляет запрос на обновление пароля пользователя

        :param request: Данные для обновления пароля пользователя
        :param user_id: Идентификатор пользователя
        :return: Ответ сервера с данными обновленного пользователя
        """

        return self.patch(url=f"{Routes.USERS}/{user_id}/password", json=request.model_dump())

    @tracker.track_coverage_httpx(f"{Routes.USERS}/" + "{user_id}")
    @allure.step("Отправка запроса на удаление пользователя")
    def delete_user_api(self,
                        *,
                        user_id: int
                        ) -> Response:
        """
        Отправляет запрос на удаление пользователя

        :param user_id: Идентификатор пользователя
        :return: Ответ сервера с сообщением об успешном удалении
        """

        return self.delete(url=f"{Routes.USERS}/{user_id}")


def get_private_user_client(
        *,
        user: LoginRequestSchema
) -> UserAPIClient:
    """
    Создает приватный HTTP клиент пользователя для доступа к API пользователей

    :param user: Данные пользователя для авторизации
    :return: Приватный HTTP клиент
    """

    return UserAPIClient(client=private_user_client_builder(user=user))

def get_private_admin_client() -> UserAPIClient:
    """
    Создает приватный HTTP клиент администратора для доступа к API пользователей

    :return: Приватный HTTP клиент
    """

    return UserAPIClient(client=private_admin_client_builder())

