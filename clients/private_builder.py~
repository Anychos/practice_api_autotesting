from httpx import Client

from clients.authentication.client import get_login_client
from clients.authentication.schemas import LoginRequestSchema
from config import settings


def get_private_client(user: LoginRequestSchema) -> Client:
    client = get_login_client()
    request = LoginRequestSchema(email=user.email, password=user.password)

    response = client.login(request)
    token = response.access_token
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {token}"}
    )
