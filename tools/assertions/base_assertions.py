from typing import Any, Sized

import allure
from jsonschema.validators import validate, Draft202012Validator


@allure.step("Проверка соответствия статус кода ответа. Ожидался {expected}, получен {actual}")
def assert_status_code(
        actual: int,
        expected: int
) -> None:
    """
    Функция для проверки статус кода

    :param actual: Полученный статус код
    :param expected: Ожидаемый статус код
    """

    assert actual == expected, (
        f"Некорректный код ответа. Получен: {actual}, ожидался: {expected}"
    )


@allure.step("Проверка соответствия значения в поле {field_name}. Ожидалось {expected}, получено {actual}")
def assert_value(
        actual: Any,
        expected: Any,
        field_name: str
) -> None:
    """
    Функция для проверки значения в поле ответа

    :param actual: Полученное значение
    :param expected: Ожидаемое значение
    :param field_name: Наименование поля
    """

    assert actual == expected, (
        f"Некорректное значение в поле {field_name}. Получено: {actual}, ожидалось: {expected}"
    )


@allure.step("Проверка наличия поля {field_name} в ответе")
def assert_field_exists(
        actual: Any,
        field_name: str
) -> None:
    """
    Проверяет, что поле присутствует в ответе

    :param field_name: Название проверяемого поля
    :param actual: Фактическое значение
    """

    assert actual is not None, (
        f"Поле {field_name} отсутствует в ответе"
    )


@allure.step("Проверка длины объекта {name}. Ожидалась {expected}, получена {actual}")
def assert_length(
        actual: Sized,
        expected: Sized,
        name: str
) -> None:
    """
    Проверяет, что длины двух объектов совпадают

    :param name: Название проверяемого объекта
    :param actual: Фактическая длина
    :param expected: Ожидаемая длина
    """

    assert len(actual) == len(expected), (
        f"Некорректная длина объекта: {name}\n"
        f"Ожидаемая длина: {len(expected)}\n"
        f"Фактическая длина: {len(actual)}"
    )


@allure.step("Валидация JSON схемы ответа")
def assert_json_schema(
        *,
        actual: Any,
        schema: dict
) -> None:
    """
    Проверяет, соответствует ли JSON в ответе заданной схеме

    :param actual: Ответ в формате JSON
    :param schema: Ожидаемая JSON схема
    """

    validate(
        instance=actual,
        schema=schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER
    ), "JSON в ответе не соответствует схеме"
