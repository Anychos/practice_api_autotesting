import platform
import sys

from config import settings


def create_allure_environment_file():
    """
    Создает файл с информацией об окружении для добавления в отчет Allure
    """
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]

    os_info = platform.platform()
    items.append(f'os={os_info}')
    items.append(f'python_version={sys.version}')

    properties = '\n'.join(items)

    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)
