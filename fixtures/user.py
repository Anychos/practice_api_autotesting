from typing import Callable

import pytest
from pydantic import BaseModel

from clients.authentication.schemas import LoginRequestSchema
from clients.user.client import UserAPIClient, get_public_user_client, get_private_user_client
from clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema


class UserFixture(BaseModel):
    """
    Хранит данные о созданном пользователе
    """

    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def user_id(self) -> int:
        return self.response.id

    @property
    def email(self) -> str:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def user_schema(self) -> LoginRequestSchema:
        schema = LoginRequestSchema(
            email=self.request.email,
            password=self.request.password
        )
        return schema


@pytest.fixture
def create_user_factory(public_user_client: UserAPIClient) -> Callable[..., UserFixture]:
    """
    Возвращает фабрику для создания пользователя

    :param public_user_client: Публичный HTTP клиент для доступа к API пользователя
    :return: Фабрика для создания пользователя
    """

    def _create_user(
            *,
            is_admin: bool = False
    ) -> UserFixture:
        """
        Создает пользователя с указанными параметрами

        :param is_admin: Флаг администратора
        :return: Объект UserFixture с информацией о пользователе
        """

        request = CreateUserRequestSchema(is_admin=is_admin)
        response = public_user_client.create_user(request)
        return UserFixture(request=request, response=response)

    return _create_user


@pytest.fixture
def public_user_client() -> UserAPIClient:
    """
    Возвращает готовый публичный HTTP клиент для доступа к API пользователя

    :return: Публичный HTTP клиент для работы с API пользователя
    """

    return get_public_user_client()

@pytest.fixture
def private_user_client(create_user_factory: Callable[..., UserFixture]) -> UserAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа пользователя к API пользователя

    :param create_user_factory: Фабрика для создания пользователя
    :return: Приватный HTTP клиент для работы пользователя с API пользователя
    """

    user = create_user_factory()
    return get_private_user_client(user=user.user_schema)

@pytest.fixture
def private_admin_client(create_user_factory: Callable[..., UserFixture]) -> UserAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа администратора к API пользователя

    :param create_user_factory: Фабрика для создания пользователя
    :return: Приватный HTTP клиент для работы администратора с API пользователя
    """

    admin = create_user_factory(is_admin=True)
    return get_private_user_client(user=admin.user_schema)



