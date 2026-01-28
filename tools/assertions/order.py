from typing import List

import allure

from clients.error_shemas import HTTPValidationErrorResponseSchema
from clients.order.schemas import CreateOrderResponseSchema, GetOrderResponseSchema, CreateOrderRequestSchema, \
    GetOrdersResponseSchema
from tools.assertions.base_assertions import assert_value, assert_field_exists
from tools.assertions.error import assert_http_validation_error_response


@allure.step("Проверка ответа на запрос создания заказа")
def assert_create_order_response(
        *,
        actual: CreateOrderResponseSchema,
        expected: CreateOrderRequestSchema
) -> None:
    assert_value(actual.cart_id, expected.cart_id, "cart_id")
    assert_field_exists(actual.id, "order_id")
    assert_field_exists(actual.user_id, "user_id")
    assert_field_exists(actual.created_at, "created_at")


@allure.step("Проверка ответа на запрос получения заказа")
def assert_get_order_response(
        *,
        actual: GetOrderResponseSchema,
        expected: CreateOrderResponseSchema
) -> None:
    assert_value(actual.id, expected.id, "id")
    assert_value(actual.cart_id, expected.cart_id, "cart_id")
    assert_value(actual.created_at, expected.created_at, "created_at")
    assert_value(actual.user_id, expected.user_id, "user_id")


@allure.step("Проверка ответа на запрос получения списка заказов")
def assert_get_orders_response(
        *,
        get_orders_response: GetOrdersResponseSchema,
        create_order_responses: List[CreateOrderResponseSchema]
) -> None:
    assert get_orders_response, "Список заказов пуст"

    orders_by_id = {
        order.id: order for order in get_orders_response
    }

    for created_order in create_order_responses:
        assert created_order.id in orders_by_id, (
            f"Заказ с id {created_order.id} отсутствует в ответе"
        )

        actual_order = orders_by_id[created_order.id]
        assert_get_order_response(actual=actual_order, expected=created_order)


@allure.step("Проверка ответа на запрос создания заказа с пустой корзиной")
def assert_empty_cart_order_response(actual: HTTPValidationErrorResponseSchema) -> None:
    expected = HTTPValidationErrorResponseSchema(
        detail="Нельзя создать заказ с пустой корзиной"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)


@allure.step("Проверка ответа на запрос создания заказа с недоступным продуктом")
def assert_unavailable_product_order_response(actual: HTTPValidationErrorResponseSchema) -> None:
    expected = HTTPValidationErrorResponseSchema(
        detail="В корзине есть недоступные для заказа товары"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)

