from http import HTTPStatus

import allure
import pytest

from clients.cart.client import CartAPIClient
from clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema, GetCartResponseSchema, \
    DeleteCartItemResponseSchema, UpdateCartItemRequestSchema, UpdateCartItemResponseSchema, DeleteCartResponseSchema
from fixtures.cart import CartFixture
from fixtures.product import ProductFixture
from tools.assertions.base_assertions import assert_status_code, assert_json_schema
from tools.assertions.cart import assert_add_item_to_cart_response, assert_get_cart_response, \
    assert_delete_item_cart_response, assert_update_cart_response, assert_delete_cart_response
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.story import Story
from tools.allure.parent_suite import ParentSuite
from tools.allure.suite import Suite
from tools.allure.sub_suite import SubSuite
from tools.allure.severity import Severity
from tools.allure.tag import Tag


@pytest.mark.regression
@pytest.mark.cart
@allure.epic(Epic.USER)
@allure.feature(Feature.CARTS)
@allure.parent_suite(ParentSuite.USER)
@allure.suite(Suite.CARTS)
@allure.tag(Tag.CARTS, Tag.REGRESSION)
class TestCart:
    @pytest.mark.smoke
    @allure.story(Story.CREATE_ENTITY)
    @allure.sub_suite(SubSuite.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.tag(Tag.SMOKE)
    def test_add_item_to_cart(self, private_cart_client: CartAPIClient, create_product: ProductFixture):
        request = AddItemCartRequestSchema(product_id=create_product.product_id)

        response = private_cart_client.add_item_cart_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = AddItemCartResponseSchema.model_validate_json(response.text)
        assert_add_item_to_cart_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.story(Story.GET_ENTITY)
    @allure.sub_suite(SubSuite.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.tag(Tag.SMOKE)
    def test_get_cart(self, private_cart_client: CartAPIClient, create_cart: CartFixture):
        response = private_cart_client.get_cart_api()
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetCartResponseSchema.model_validate_json(response.text)
        assert_get_cart_response(response_data, [create_cart.response])
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.DELETE_ENTITY)
    @allure.sub_suite(SubSuite.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_remove_item_from_cart(self, private_cart_client: CartAPIClient, create_cart: CartFixture):
        response = private_cart_client.remove_item_cart_api(item_id=create_cart.item_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = DeleteCartItemResponseSchema.model_validate_json(response.text)
        assert_delete_item_cart_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.UPDATE_ENTITY)
    @allure.sub_suite(SubSuite.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_update_cart(self, private_cart_client: CartAPIClient, create_cart: CartFixture):
        request = UpdateCartItemRequestSchema()

        response = private_cart_client.update_cart_item_api(item_id=create_cart.item_id, request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateCartItemResponseSchema.model_validate_json(response.text)
        assert_update_cart_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.DELETE_ENTITY)
    @allure.sub_suite(SubSuite.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_delete_cart(self, private_cart_client: CartAPIClient, create_cart: CartFixture):
        response = private_cart_client.delete_cart_api()
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = DeleteCartResponseSchema.model_validate_json(response.text)
        assert_delete_cart_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())
