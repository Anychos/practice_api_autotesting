from httpx import Client

from clients.event_hooks import request_curl_event_hook
from config import settings


def get_public_client() -> Client:
    """
    Создает публичный HTTP клиент для доступа к открытому API

    :return: Публичный HTTP клиент
    """
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        event_hooks={"request": [request_curl_event_hook]}
    )
