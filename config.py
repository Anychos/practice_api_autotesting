from pydantic import BaseModel, HttpUrl, FilePath
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

settings = Settings()
