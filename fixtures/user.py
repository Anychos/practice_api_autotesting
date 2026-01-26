from typing import Callable

import pytest
from pydantic import BaseModel

from clients.authentication.schemas import LoginRequestSchema
from clients.user.client import UserAPIClient, get_private_admin_client, \
    get_private_user_client
from clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema
from config import settings


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
def private_admin_client() -> UserAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа администратора к API пользователя

    :return: Приватный HTTP клиент для работы администратора с API пользователя
    """

    return get_private_admin_client()

@pytest.fixture
def create_user_factory(private_admin_client: UserAPIClient) -> Callable[..., UserFixture]:
    """
    Возвращает фабрику для создания пользователя

    :param private_admin_client: приватный HTTP клиент для доступа администратора к API пользователя
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
        response = private_admin_client.create_user(request=request)
        return UserFixture(request=request, response=response)

    return _create_user

@pytest.fixture
def user(create_user_factory: Callable[..., UserFixture]) -> UserFixture:
    """
    Возвращает готового пользователя

    :param create_user_factory: Фабрика для создания пользователя
    :return: Объект UserFixture с информацией о пользователе
    """

    return create_user_factory()

@pytest.fixture
def private_user_client(user: UserFixture) -> UserAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа пользователя к API пользователя

    :param user: Созданный пользователь
    :return: Приватный HTTP клиент для работы пользователя с API пользователя
    """

    return get_private_user_client(user=user.user_schema)

@pytest.fixture
def admin(create_user_factory: Callable[..., UserFixture]) -> UserFixture:
    """
    Возвращает готового администратора

    :param create_user_factory: Фабрика для создания пользователя
    :return: Объект UserFixture с информацией об администраторе
    """

    return create_user_factory(is_admin=True)



