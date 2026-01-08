from http import HTTPStatus

import allure
import pytest

from clients.user.client import UserAPIClient
from clients.user.schemas import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, \
    UpdateUserResponseSchema, UpdateUserRequestSchema
from fixtures.user import UserFixture
from tools.assertions.base_assertions import assert_status_code, assert_json_schema
from tools.assertions.user import assert_create_user_response, assert_get_user_response, assert_update_user_response
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.story import Story
from tools.allure.severity import Severity
from tools.allure.tag import Tag


@pytest.mark.regression
@pytest.mark.user
@allure.epic(Epic.USER)
@allure.feature(Feature.USERS)
@allure.tag(Tag.USERS, Tag.REGRESSION)
class TestUserPositive:
    @pytest.mark.smoke
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.tag(Tag.SMOKE)
    def test_create_user(self, public_user_client: UserAPIClient):
        request = CreateUserRequestSchema()

        response = public_user_client.create_user_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        assert_create_user_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_get_user(self, private_user_client: UserAPIClient, user: UserFixture):
        response = private_user_client.get_user_api(user_id=user.user_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetUserResponseSchema.model_validate_json(response.text)
        assert_get_user_response(response_data, user.response)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.UPDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_update_user(self, private_user_client: UserAPIClient, user: UserFixture):
        request = UpdateUserRequestSchema()

        response = private_user_client.update_user_api(user_id=user.user_id, request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateUserResponseSchema.model_validate_json(response.text)
        assert_update_user_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.DELETE_ENTITY)
    @allure.severity(Severity.MINOR)
    def test_delete_user(self, private_user_client: UserAPIClient, user: UserFixture):
        response = private_user_client.delete_user_api(user_id=user.user_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

@pytest.mark.regression
@pytest.mark.user
@allure.epic(Epic.USER)
@allure.feature(Feature.USERS)
@allure.tag(Tag.USERS, Tag.REGRESSION)
class TestUserNegative:
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_user_wrong_email(self):
        pass

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_user_wrong_password(self):
        pass

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_user_wrong_phone(self):
        pass

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_user_without_required_field(self):
        pass

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_user_existing_email(self):
        pass
