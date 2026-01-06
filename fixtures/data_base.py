import pytest

from clients.data_base.client import get_data_base_client, DataBaseAPIClient


@pytest.fixture(scope="session")
def data_base_client() -> DataBaseAPIClient:
    return get_data_base_client()

@pytest.fixture(scope="session")
def clear_data_base_session(data_base_client: DataBaseAPIClient) -> None:
    data_base_client.clear_data_base_api()

@pytest.fixture
def clear_data_base_function(clear_data_base_session) -> None:
    print("Очистка БД перед тестом")
