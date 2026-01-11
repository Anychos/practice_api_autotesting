from http import HTTPStatus

import allure
import pytest

from clients.authentication.client import AuthenticationAPIClient
from clients.authentication.schemas import LoginRequestSchema, LoginResponseSchema
from clients.error_shemas import HTTPValidationErrorResponseSchema, InputValidationErrorResponseSchema
from fixtures.user import UserFixture
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.severity import Severity
from tools.allure.story import Story
from tools.assertions.authentication import assert_login_response, assert_wrong_login_data_response, \
    assert_invalid_email_format_response
from tools.assertions.base_assertions import assert_status_code, assert_json_schema


@pytest.mark.regression
@pytest.mark.authentication
@allure.feature(Feature.AUTHENTICATION)
@allure.story(Story.LOGIN)
class TestAuthenticationPositive:
    @pytest.mark.smoke
    @allure.epic(Epic.USER)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Логин пользователя с валидными данными")
    def test_user_login(self, auth_client: AuthenticationAPIClient, user: UserFixture):
        request = LoginRequestSchema(email=user.email, password=user.password)

        response = auth_client.login_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = LoginResponseSchema.model_validate_json(response.text)
        assert_login_response(response_data, user.request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.epic(Epic.ADMIN)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Логин админа с валидными данными")
    def test_admin_login(self, auth_client: AuthenticationAPIClient, admin: UserFixture):
        request = LoginRequestSchema(email=admin.email, password=admin.password)

        response = auth_client.login_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = LoginResponseSchema.model_validate_json(response.text)
        assert_login_response(response_data, admin.request)
        assert_json_schema(response.json(), response_data.model_json_schema())

@pytest.mark.regression
@pytest.mark.authentication
@allure.feature(Feature.AUTHENTICATION)
@allure.story(Story.LOGIN)
class TestAuthenticationNegative:
    @allure.epic(Epic.USER)
    @allure.severity(Severity.NORMAL)
    @allure.title("Логин пользователя с валидным, но не зарегистрированным email и валидным паролем")
    def test_user_login_unregistered_email(self, auth_client: AuthenticationAPIClient, user: UserFixture):
        request = LoginRequestSchema(email="test@mail.ru", password=user.password)

        response = auth_client.login_api(request)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_login_data_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.epic(Epic.USER)
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize("email", ["test@mail", "test@.ru", "@mail.ru", ""])
    @allure.title("Логин пользователя с невалидным форматом email и валидным паролем")
    def test_user_login_invalid_email_format(self, auth_client: AuthenticationAPIClient, email: str, user: UserFixture):
        request = LoginRequestSchema(email=email, password=user.password)

        response = auth_client.login_api(request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_invalid_email_format_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.epic(Epic.USER)
    @allure.severity(Severity.NORMAL)
    @allure.title("Логин пользователя с зарегистрированным email и неподходящим паролем")
    def test_user_login_inappropriate_password(self, auth_client: AuthenticationAPIClient, user: UserFixture):
        request = LoginRequestSchema(email=user.email, password="wrong_password_123")

        response = auth_client.login_api(request)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_login_data_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.epic(Epic.USER)
    @allure.severity(Severity.NORMAL)
    @allure.title("Логин пользователя с отсутствующим паролем")
    def test_user_login_empty_password(self, auth_client: AuthenticationAPIClient, user: UserFixture):
        request = LoginRequestSchema(email=user.email, password="")

        response = auth_client.login_api(request)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_login_data_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())


