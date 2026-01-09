import allure
from httpx import Request

from tools.http.curl import get_curl_from_request


def request_curl_event_hook(request: Request):
    curl_command = get_curl_from_request(request)

    allure.attach(curl_command, "cURL", attachment_type=allure.attachment_type.TEXT)
