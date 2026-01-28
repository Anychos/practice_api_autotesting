from http import HTTPStatus

import allure
import pytest

from clients.authentication.client import AuthenticationAPIClient
from clients.authentication.schemas import LoginRequestSchema, LoginResponseSchema, RegistrationRequestSchema, \
    RegistrationResponseSchema
from clients.error_shemas import HTTPValidationErrorResponseSchema, InputValidationErrorResponseSchema
from fixtures.user import UserFixture
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.severity import Severity
from tools.allure.story import Story
from tools.assertions.authentication import assert_login_response, assert_wrong_login_data_response, \
    assert_invalid_email_format_response, assert_register_response, assert_already_registered_email_response
from tools.assertions.base_assertions import assert_status_code, assert_json_schema


@pytest.mark.regression
@pytest.mark.authentication
@allure.feature(Feature.AUTHENTICATION)
class TestAuthenticationPositive:
    @pytest.mark.smoke
    @allure.epic(Epic.USER)
    @allure.story(Story.REGISTRATION)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Регистрация пользователя с валидными данными")
    def test_user_registration(self,
                              auth_client: AuthenticationAPIClient
                              ) -> None:
        request = RegistrationRequestSchema()

        response = auth_client.registration_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = RegistrationResponseSchema.model_validate_json(response.text)
        assert_register_response(actual=response_data, expected=request)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.epic(Epic.USER)
    @allure.story(Story.LOGIN)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Логин пользователя с валидными данными")
    def test_user_login(self,
                        auth_client: AuthenticationAPIClient,
                        user: UserFixture
                        ) -> None:
        request = LoginRequestSchema(email=user.email, password=user.password)

        response = auth_client.login_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = LoginResponseSchema.model_validate_json(response.text)
        assert_login_response(actual=response_data, expected=user.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.epic(Epic.ADMIN)
    @allure.story(Story.LOGIN)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Логин админа с валидными данными")
    def test_admin_login(self,
                         auth_client: AuthenticationAPIClient,
                         admin: UserFixture
                         ) -> None:
        request = LoginRequestSchema(email=admin.email, password=admin.password)

        response = auth_client.login_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = LoginResponseSchema.model_validate_json(response.text)
        assert_login_response(actual=response_data, expected=admin.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())


@pytest.mark.regression
@pytest.mark.authentication
@allure.feature(Feature.AUTHENTICATION)
class TestAuthenticationNegative:
    @allure.epic(Epic.USER)
    @allure.story(Story.REGISTRATION)
    @allure.severity(Severity.NORMAL)
    @allure.title("Регистрация пользователя с зарегистрированным email")
    def test_user_registration_registered_email(self,
                                                auth_client: AuthenticationAPIClient,
                                                user: UserFixture
                                                ) -> None:
        request = RegistrationRequestSchema(email=user.email)

        response = auth_client.registration_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_already_registered_email_response(actual=response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.epic(Epic.USER)
    @allure.story(Story.LOGIN)
    @allure.severity(Severity.NORMAL)
    @allure.title("Логин пользователя с валидным, но не зарегистрированным email и валидным паролем")
    def test_user_login_unregistered_email(self,
                                           auth_client: AuthenticationAPIClient,
                                           user: UserFixture
                                           ) -> None:
        request = LoginRequestSchema(email="test@mail.ru", password=user.password)

        response = auth_client.login_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_login_data_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.epic(Epic.USER)
    @allure.story(Story.LOGIN)
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize("email",
                             ["test@mail.",
                              "test@.ru",
                              "@mail.ru",
                              "",
                              "testmail.ru"]
                             )
    @allure.title("Логин пользователя с невалидным форматом email и валидным паролем")
    def test_user_login_invalid_email_format(self,
                                             auth_client: AuthenticationAPIClient,
                                             email: str,
                                             user: UserFixture
                                             ) -> None:
        request = LoginRequestSchema.model_construct(email=email, password=user.password)

        response = auth_client.login_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_invalid_email_format_response(actual=response_data, email=email)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.epic(Epic.USER)
    @allure.story(Story.LOGIN)
    @allure.severity(Severity.NORMAL)
    @allure.title("Логин пользователя с зарегистрированным email и неподходящим паролем")
    def test_user_login_inappropriate_password(self,
                                               auth_client: AuthenticationAPIClient,
                                               user: UserFixture
                                               ) -> None:
        request = LoginRequestSchema(email=user.email, password="wrong_password_123")

        response = auth_client.login_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_login_data_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.epic(Epic.USER)
    @allure.story(Story.LOGIN)
    @allure.severity(Severity.NORMAL)
    @allure.title("Логин пользователя с отсутствующим паролем")
    def test_user_login_empty_password(self,
                                       auth_client: AuthenticationAPIClient,
                                       user: UserFixture
                                       ) -> None:
        request = LoginRequestSchema(email=user.email, password="")

        response = auth_client.login_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_login_data_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())


