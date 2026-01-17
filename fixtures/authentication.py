import pytest

from clients.authentication.client import AuthenticationAPIClient, get_login_client


@pytest.fixture
def auth_client() -> AuthenticationAPIClient:
    """
    Возвращает готовый HTTP клиент для доступа к API аутентификации

    :return: HTTP клиент для работы с API аутентификации
    """

    return get_login_client()
