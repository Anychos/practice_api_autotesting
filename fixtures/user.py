import pytest
from pydantic import BaseModel

from clients.authentication.schemas import LoginRequestSchema
from clients.user.client import UserAPIClient, get_public_user_client, get_private_user_client
from clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema


class UserFixture(BaseModel):
    """
    Модель хранит данные о созданном пользователе
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

def create_user_fixture(public_user_client: UserAPIClient, is_admin: bool) -> UserFixture:
    """
    Создает пользователя

    :param public_user_client: Публичный HTTP клиент для доступа к API пользователей
    :param is_admin: Флаг администратора
    :return: Информация о созданном пользователе
    """
    request = CreateUserRequestSchema(is_admin=is_admin)
    response = public_user_client.create_user(request)
    return UserFixture(request=request, response=response)

@pytest.fixture
def user(public_user_client: UserAPIClient) -> UserFixture:
    """
    Создает пользователя

    :param public_user_client: Публичный HTTP клиент для доступа к API пользователей
    :return: Информация о созданном пользователе
    """
    return create_user_fixture(public_user_client, is_admin=False)

@pytest.fixture
def admin(public_user_client: UserAPIClient) -> UserFixture:
    """
    Создает администратора

    :param public_user_client: Публичный HTTP клиент для доступа к API пользователей
    :return: Информация об созданном администраторе
    """
    return create_user_fixture(public_user_client, is_admin=True)

@pytest.fixture
def public_user_client() -> UserAPIClient:
    """
    Возвращает готовый публичный HTTP клиент для доступа к API пользователей

    :return: HTTP клиент
    """
    return get_public_user_client()

@pytest.fixture
def private_user_client(user: UserFixture) -> UserAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа пользователя к API пользователей

    :param user: Пользователь
    :return: HTTP клиент
    """
    return get_private_user_client(user=user.user_schema)

@pytest.fixture
def private_admin_client(admin: UserFixture) -> UserAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа администратора к API пользователей

    :param admin: Администратор
    :return: HTTP клиент
    """
    return get_private_user_client(user=admin.user_schema)



