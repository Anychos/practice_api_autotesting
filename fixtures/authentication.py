import pytest

from clients.authentication.client import AuthenticationAPIClient, get_login_client


@pytest.fixture
def auth_client() -> AuthenticationAPIClient:
    return get_login_client()
