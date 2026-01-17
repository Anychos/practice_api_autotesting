from httpx import Request, RequestNotRead


def get_curl_from_request(request: Request) -> str:
    """
    Формирует cURL команду из запроса

    :param request: Запрос для извлечения cURL команды
    :return: cURL команда
    """
    result: list[str] = [f"curl -X '{request.method}' '{request.url}'"]

    for header, value in request.headers.items():
        result.append(f"-H '{header}: {value}'")

    try:
        if body :=request.content:
            result.append(f"-d '{body.decode('utf-8')}'")
    except RequestNotRead:
        pass

    return " \\\n ".join(result)
