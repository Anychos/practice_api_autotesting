from http import HTTPStatus

import allure
import pytest

from clients.error_shemas import InputValidationErrorResponseSchema, HTTPValidationErrorResponseSchema
from clients.user.client import UserAPIClient
from clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, \
    UpdateUserResponseSchema, UpdateUserRequestSchema
from fixtures.user import UserFixture
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.severity import Severity
from tools.allure.story import Story
from tools.assertions.authentication import assert_invalid_email_format_response
from tools.assertions.base_assertions import assert_status_code, assert_json_schema
from tools.assertions.user import assert_create_user_response, assert_get_user_response, assert_update_user_response, \
    assert_wrong_password_response, assert_wrong_phone_response, assert_email_exists_response


@pytest.mark.regression
@pytest.mark.user
@allure.epic(Epic.USER)
@allure.feature(Feature.USERS)
class TestUserPositive:
    @pytest.mark.smoke
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Создание пользователя с валидными данными")
    def test_create_user(self, public_user_client: UserAPIClient):
        request = CreateUserRequestSchema()

        response = public_user_client.create_user_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        assert_create_user_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Получение существующего пользователя")
    def test_get_user(self, private_user_client: UserAPIClient, user: UserFixture):
        response = private_user_client.get_user_api(user_id=user.user_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetUserResponseSchema.model_validate_json(response.text)
        assert_get_user_response(response_data, user.response)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.UPDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Обновление данных существующего пользователя")
    def test_update_user(self, private_user_client: UserAPIClient, user: UserFixture):
        request = UpdateUserRequestSchema()

        response = private_user_client.update_user_api(user_id=user.user_id, request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateUserResponseSchema.model_validate_json(response.text)
        assert_update_user_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.DELETE_ENTITY)
    @allure.severity(Severity.MINOR)
    @allure.title("Удаление существующего пользователя")
    def test_delete_user(self, private_user_client: UserAPIClient, user: UserFixture):
        response = private_user_client.delete_user_api(user_id=user.user_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

@pytest.mark.regression
@pytest.mark.user
@allure.epic(Epic.USER)
@allure.feature(Feature.USERS)
class TestUserNegative:
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize("email",
                             ["test@mail",
                              "test@.ru",
                              "@mail.ru",
                              ""]
                             )
    @allure.title("Создание пользователя с невалидным email")
    def test_create_user_wrong_email(self, public_user_client: UserAPIClient, email: str):
        request = CreateUserRequestSchema(email=email)

        response = public_user_client.create_user_api(request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_invalid_email_format_response(response_data, email=email)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize("password",
                             ["qwert",
                              "goxtKsdqYKIzmIFOTwkYOXNmermrTsShEpEhCjrvojfKZILuibjEXMPFGVsewfFuyvkQOXCmJippSdAuZoxGTaUSutgeizZygQgyEPIbADJhOGBQYgAaFAxeANhwzcwGr",
                              ""]
                             )
    @allure.title("Создание пользователя с невалидным паролем")
    def test_create_user_wrong_password(self, public_user_client: UserAPIClient, password: str):
        request = CreateUserRequestSchema(password=password)

        response = public_user_client.create_user_api(request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_password_response(response_data, password=password)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize("phone",
                             ["phonenumber",
                              "123456789",
                              "1234567890112",
                              "7(793)456-78-90",
                              ""]
                             )
    @allure.title("Создание пользователя с невалидным телефоном")
    def test_create_user_wrong_phone(self, public_user_client: UserAPIClient, phone: str):
        request = CreateUserRequestSchema(phone=phone)

        response = public_user_client.create_user_api(request)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        response_data = InputValidationErrorResponseSchema.model_validate_json(response.text)
        assert_wrong_phone_response(response_data, phone=phone)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Создание пользователя с уже зарегистрированным email")
    def test_create_user_existing_email(self, public_user_client: UserAPIClient, user: UserFixture):
        request = CreateUserRequestSchema(email=user.email)

        response = public_user_client.create_user_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_email_exists_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())
