import allure

from clients.error_shemas import InputValidationErrorResponseSchema, HTTPValidationErrorResponseSchema
from clients.user.schemas import CreateUserResponseSchema, CreateUserRequestSchema, GetUserResponseSchema, \
    UserSchema, UpdateUserResponseSchema, UpdateUserRequestSchema, DeleteUserResponseSchema
from tools.assertions.base_assertions import assert_field_exists, assert_value


@allure.step("Проверка данных пользователя по схеме")
def assert_user(actual: UserSchema, expected: UserSchema) -> None:
    assert_value(actual.email, expected.email, "email")
    assert_value(actual.name, expected.name, "name")
    assert_value(actual.phone, expected.phone, "phone")

@allure.step("Проверка ответа на запрос создания пользователя")
def assert_create_user_response(actual: CreateUserResponseSchema, expected: CreateUserRequestSchema) -> None:
    assert_field_exists(actual.id, "id")
    assert_field_exists(actual.is_admin, "is_admin")
    assert_user(actual, expected)

@allure.step("Проверка ответа на запрос получения пользователя")
def assert_get_user_response(actual: GetUserResponseSchema, expected: CreateUserResponseSchema) -> None:
    assert_value(actual.id, expected.id, "id")
    assert_user(actual, expected)

@allure.step("Проверка ответа на запрос обновления пользователя")
def assert_update_user_response(actual: UpdateUserResponseSchema, expected: UpdateUserRequestSchema) -> None:
    assert_field_exists(actual.id, "id")
    assert_value(actual.email, expected.email, "email")
    assert_value(actual.name, expected.name, "name")
    assert_value(actual.phone, expected.phone, "phone")
    assert_value(actual.is_admin, False, "is_admin")

@allure.step("Проверка ответа на запрос удаления пользователя")
def assert_delete_user_response(actual: DeleteUserResponseSchema) -> None:
    assert_value(actual.message, "User deleted successfully", "message")

@allure.step("Проверка ответа на запрос с некорректным паролем")
def assert_wrong_password_response(actual: InputValidationErrorResponseSchema) -> None:
    warnings = [
        "Value error, Password must be at least 6 characters long",
        "Value error, Password must be at most 128 characters long"
    ]

    assert actual.detail, "Список ошибок пуст"

    error = actual.detail[0]

    assert error.type == "value_error"
    assert error.location == ["body", "password"]

    assert any(
        warning in error.message
        for warning in warnings
    ), f"Неожиданная ошибка: {error.message}"

    assert error.context, "Контекст ошибки пуст"

    if error.context is not None: assert any(
        warning in error.context
        for warning in warnings
    ), f"Неожиданная ошибка: {error.context}"

@allure.step("Проверка ответа на запрос с некорректным номером телефона")
def assert_wrong_phone_response(actual: InputValidationErrorResponseSchema) -> None:
    warnings = [
        "Value error, Phone number is too long",
        "Value error, Phone number is too short",
        "Value error, Phone number must contain only digits and optional + at the beginning",
        "Value error, Phone number cannot be empty"
    ]

    assert actual.detail, "Список ошибок пуст"

    error = actual.detail[0]

    assert error.type == "value_error"
    assert error.location == ["body", "phone"]

    assert any(
        warning in error.message
        for warning in warnings
    ), f"Неожиданная ошибка: {error.message}"

    assert error.context, "Контекст ошибки пуст"

    if error.context is not None: assert any(
        warning in error.context
        for warning in warnings
    ), f"Неожиданная ошибка: {error.context}"

@allure.step("Проверка ответа на запрос с уже зарегистрированным email")
def assert_email_exists_response(actual: HTTPValidationErrorResponseSchema) -> None:
    assert_value(actual.detail, "Email already registered", "detail")
