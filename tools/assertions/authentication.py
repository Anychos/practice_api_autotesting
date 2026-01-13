import allure

from clients.authentication.schemas import LoginResponseSchema
from clients.error_shemas import HTTPValidationErrorResponseSchema, InputValidationErrorResponseSchema, ErrorSchema
from clients.user.schemas import CreateUserRequestSchema
from tools.assertions.base_assertions import assert_field_exists, assert_value
from tools.assertions.error import assert_http_validation_error_response, assert_input_validation_error_response
from tools.assertions.user import assert_user


@allure.step("Проверка ответа на запрос логина пользователя")
def assert_login_response(actual: LoginResponseSchema, expected: CreateUserRequestSchema) -> None:
    assert_field_exists(actual.access_token, "access_token")
    assert_value(actual.token_type, "bearer", "token_type")
    assert_field_exists(actual.user.id, "user_id")
    assert_user(actual.user, expected)

@allure.step("Проверка ответа на запрос логина пользователя с некорректными данными")
def assert_wrong_login_data_response(actual: HTTPValidationErrorResponseSchema) -> None:
    expected = HTTPValidationErrorResponseSchema(
        detail="Incorrect email or password"
    )
    assert_http_validation_error_response(actual, expected)

@allure.step("Проверка ответа на запрос логина пользователя с некорректным форматом email")
def assert_invalid_email_format_response(
    actual: InputValidationErrorResponseSchema,
    email: str) -> None:
    error_messages = [
        "The part after the @-sign is not valid. It should have a period.",
        "An email address cannot end with a period.",
        "An email address cannot have a period immediately after the @-sign.",
        "There must be something before the @-sign.",
        "An email address must have an @-sign.",
    ]

    assert actual.detail, "Список ошибок пуст"
    assert len(actual.detail) == 1, "В ответе более одной ошибки"

    error = actual.detail[0]

    assert error.type == "value_error"
    assert error.location == ["body", "email"]
    assert any(message in error.message for message in error_messages), (
        f"Неожиданная ошибка: {error.message}"
    )
    assert error.input == email
    assert error.context, "Контекст ошибки отсутствует"
    assert "reason" in error.context

