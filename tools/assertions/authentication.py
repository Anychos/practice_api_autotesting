import allure

from clients.authentication.schemas import LoginResponseSchema
from clients.user.schemas import CreateUserRequestSchema
from tools.assertions.base_assertions import assert_field_exists, assert_value
from tools.assertions.user import assert_user


@allure.step("Проверка ответа на запрос логина пользователя")
def assert_login_response(actual: LoginResponseSchema, expected: CreateUserRequestSchema) -> None:
    assert_field_exists(actual.access_token, "access_token")
    assert_value(actual.token_type, "bearer", "token_type")
    assert_field_exists(actual.user.id, "user_id")
    assert_user(actual.user, expected)
