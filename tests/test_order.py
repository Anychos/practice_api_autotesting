from http import HTTPStatus
from typing import Callable

import allure
import pytest

from clients.error_shemas import HTTPValidationErrorResponseSchema
from clients.order.client import OrderAPIClient
from clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema, GetOrderResponseSchema
from fixtures.cart import CartFixture
from fixtures.order import OrderFixture
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.severity import Severity
from tools.allure.story import Story
from tools.assertions.base_assertions import assert_status_code, assert_json_schema
from tools.assertions.order import assert_create_order_response, assert_get_order_response, \
    assert_empty_cart_order_response, assert_unavailable_product_order_response


@pytest.mark.regression
@pytest.mark.cart
@allure.epic(Epic.USER)
@allure.feature(Feature.CARTS)
class TestOrderPositive:
    @pytest.mark.smoke
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Создание заказа")
    def test_create_order(self,
                          private_order_client: OrderAPIClient,
                          create_cart_factory: Callable[..., CartFixture]
                          ) -> None:
        cart = create_cart_factory()
        request = CreateOrderRequestSchema(cart_id=cart.cart_id)

        response = private_order_client.create_order_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateOrderResponseSchema.model_validate_json(response.text)
        assert_create_order_response(actual=response_data, expected=request)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Получение заказа по id")
    def test_get_order_by_id(self,
                             private_order_client: OrderAPIClient,
                             create_order: OrderFixture
                             ) -> None:
        response = private_order_client.get_order_api(order_id=create_order.order_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetOrderResponseSchema.model_validate_json(response.text)
        assert_get_order_response(actual=response_data, expected=create_order.response)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.GET_ENTITIES)
    @allure.severity(Severity.NORMAL)
    @allure.title("Получение списка заказов")
    def test_get_orders(self,
                        private_order_client: OrderAPIClient,
                        create_order: OrderFixture
                        ) -> None:
        response = private_order_client.get_orders_api()
        assert_status_code(response.status_code, HTTPStatus.OK)


@pytest.mark.regression
@pytest.mark.cart
@allure.epic(Epic.USER)
@allure.feature(Feature.CARTS)
class TestOrderNegative:
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Создание заказа если один из продуктов недоступен")
    @pytest.mark.skip
    def test_create_order_without_availability_items_in_cart(self,
                                                             private_order_client: OrderAPIClient,
                                                             create_cart_factory: Callable[..., CartFixture],
                                                             update_product_factory
                                                             ) -> None:
        cart = create_cart_factory(is_available=True, stock_quantity=1)
        update_product_factory(is_available=False, stock_quantity=0)

        request = CreateOrderRequestSchema(cart_id=cart.cart_id)

        response = private_order_client.create_order_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_unavailable_product_order_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Создание заказа с удаленной корзиной")
    @pytest.mark.skip
    def test_create_order_with_empty_cart(self,
                                          private_order_client: OrderAPIClient,
                                          clear_cart
                                          ) -> None:
        request = CreateOrderRequestSchema(cart_id=1)

        response = private_order_client.create_order_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_empty_cart_order_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

