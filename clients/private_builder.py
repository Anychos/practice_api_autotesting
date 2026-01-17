from httpx import Client

from clients.authentication.client import get_login_client
from clients.authentication.schemas import LoginRequestSchema
from clients.event_hooks import request_curl_event_hook
from config import settings


def get_private_client(user: LoginRequestSchema) -> Client:
    """
    Создает HTTP клиент для доступа к приватному API

    :param user: Данные пользователя для авторизации
    :return: Приватный HTTP клиент
    """

    client = get_login_client()
    request = LoginRequestSchema(email=user.email, password=user.password)

    response = client.login(request)
    token = response.access_token
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {token}"},
        event_hooks={"request": [request_curl_event_hook]}
    )
