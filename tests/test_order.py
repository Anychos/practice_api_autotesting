from http import HTTPStatus

import allure
import pytest

from clients.order.client import OrderAPIClient
from clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema, GetOrderResponseSchema
from fixtures.cart import CartFixture
from fixtures.order import OrderFixture
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.parent_suite import ParentSuite
from tools.allure.severity import Severity
from tools.allure.story import Story
from tools.allure.sub_suite import SubSuite
from tools.allure.suite import Suite
from tools.allure.tag import Tag
from tools.assertions.base_assertions import assert_status_code, assert_json_schema
from tools.assertions.order import assert_create_order_response, assert_get_order_response


@pytest.mark.regression
@pytest.mark.cart
@allure.epic(Epic.USER)
@allure.feature(Feature.CARTS)
@allure.parent_suite(ParentSuite.USER)
@allure.suite(Suite.CARTS)
@allure.tag(Tag.CARTS, Tag.REGRESSION)
class TestOrderPositive:
    @pytest.mark.smoke
    @allure.story(Story.CREATE_ENTITY)
    @allure.sub_suite(SubSuite.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.tag(Tag.SMOKE)
    def test_create_order(self, private_order_client: OrderAPIClient, create_cart: CartFixture):
        request = CreateOrderRequestSchema(cart_id=create_cart.cart_id)

        response = private_order_client.create_order_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateOrderResponseSchema.model_validate_json(response.text)
        assert_create_order_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.GET_ENTITY)
    @allure.sub_suite(SubSuite.GET_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_get_order_by_id(self, private_order_client: OrderAPIClient, create_order: OrderFixture):
        response = private_order_client.get_order_api(order_id=create_order.order_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetOrderResponseSchema.model_validate_json(response.text)
        assert_get_order_response(response_data, create_order.response)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(Story.GET_ENTITIES)
    @allure.sub_suite(SubSuite.GET_ENTITIES)
    @allure.severity(Severity.NORMAL)
    def test_get_orders(self, private_order_client: OrderAPIClient, create_order: OrderFixture):
        response = private_order_client.get_orders_api()
        assert_status_code(response.status_code, HTTPStatus.OK)

        # TODO: add assertions for list

class TestOrderNegative:
    def test_create_order_without_availability_items_in_cart(self):
        pass

