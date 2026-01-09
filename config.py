from typing import Self

from pydantic import BaseModel, HttpUrl, FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientSettings(BaseModel):
    """
    Настройки HTTP клиента
    """
    base_url: HttpUrl
    timeout: int

    @property
    def url(self) -> str:
        return str(self.base_url)

class TestDataSettings(BaseModel):
    """
    Настройки тестовых данных
    """
    image_png: FilePath
    image_jpg: FilePath
    image_jpeg: FilePath
    image_webp: FilePath
    image_heic: FilePath

class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter='.'
    )

    http_client: HTTPClientSettings
    test_data: TestDataSettings
    allure_report_dir: DirectoryPath = DirectoryPath("allure-report")

    @classmethod
    def init(cls) -> Self:
        allure_report_dir = DirectoryPath("./allure-report")
        allure_report_dir.mkdir(exist_ok=True)
        return Settings(allure_report_dir=allure_report_dir)

settings = Settings.init()
