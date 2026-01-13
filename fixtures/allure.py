import pytest

from tools.allure.enviroment import create_allure_environment_file


@pytest.fixture(scope="session", autouse=True)
def save_allure_environment_file():
    """
    Сохраняет информацию об окружении для Allure
    """
    yield
    create_allure_environment_file()
