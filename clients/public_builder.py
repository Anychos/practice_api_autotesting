from httpx import Client

from config import settings


def get_public_client() -> Client:
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout
    )
