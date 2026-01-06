import allure

from clients.user.schemas import CreateUserResponseSchema, CreateUserRequestSchema, GetUserResponseSchema, \
    FullUserSchema, UpdateUserResponseSchema, UpdateUserRequestSchema, DeleteUserResponseSchema
from tools.assertions.base_assertions import assert_field_exists, assert_value


@allure.step("Проверка данных пользователя по схеме")
def assert_user(actual: FullUserSchema, expected: FullUserSchema) -> None:
    assert_value(actual.email, expected.email, "email")
    assert_value(actual.name, expected.name, "name")
    assert_value(actual.phone, expected.phone, "phone")
    assert_value(actual.is_admin, False, "is_admin")

@allure.step("Проверка ответа на запрос создания пользователя")
def assert_create_user_response(actual: CreateUserResponseSchema, expected: CreateUserRequestSchema) -> None:
    assert_field_exists(actual.id, "id")
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
