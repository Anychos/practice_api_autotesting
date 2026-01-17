import allure
from httpx import Request

from tools.http.curl import get_curl_from_request


def request_curl_event_hook(request: Request) -> None:
    """
    Получает cURL команду из запроса и прикрепляет ее к отчету Allure

    :param request: Запрос для извлечения cURL команды
    """

    curl_command = get_curl_from_request(request)

    allure.attach(curl_command, "cURL", attachment_type=allure.attachment_type.TEXT)
