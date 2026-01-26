from typing import Self

from pydantic import BaseModel, HttpUrl, DirectoryPath
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

class AdminLoginSchema(BaseModel):
    email: str
    password: str

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
    allure_results_dir: DirectoryPath = DirectoryPath("allure-results")
    admin_data: AdminLoginSchema

    @classmethod
    def init(cls) -> Self:
        allure_results_dir = DirectoryPath("./allure-results")
        allure_results_dir.mkdir(exist_ok=True)
        return Settings(allure_results_dir=allure_results_dir)

settings = Settings.init()
