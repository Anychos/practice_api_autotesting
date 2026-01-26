from httpx import Client
from pydantic import Field, BaseModel

from clients.authentication.client import get_authentication_client
from clients.authentication.schemas import LoginRequestSchema
from clients.event_hooks import request_curl_event_hook
from config import settings


def private_user_client_builder(
        *,
        user: LoginRequestSchema
) -> Client:
    """
    Создает HTTP клиент пользователя для доступа к приватному API

    :param user: Данные пользователя для авторизации
    :return: Приватный HTTP клиент
    """

    client = get_authentication_client()
    request = LoginRequestSchema(email=user.email, password=user.password)

    response = client.login(request=request)
    token = response.access_token
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {token}"},
        event_hooks={"request": [request_curl_event_hook]}
    )


def private_admin_client_builder() -> Client:
    """
    Создает HTTP клиент администратора для доступа к приватному API

    :return: Приватный HTTP клиент
    """

    client = get_authentication_client()
    request = LoginRequestSchema(email=settings.admin_data.email, password=settings.admin_data.password)

    response = client.login(request=request)
    token = response.access_token
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {token}"},
        event_hooks={"request": [request_curl_event_hook]}
    )
