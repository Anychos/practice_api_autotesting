from typing import List

import allure

from clients.error_shemas import HTTPValidationErrorResponseSchema
from clients.order.schemas import CreateOrderResponseSchema, CreateOrderRequestSchema, GetOrderResponseSchema
from tools.assertions.base_assertions import assert_value, assert_field_exists


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
    assert_create_order_response(actual=actual, expected=expected)


@allure.step("Проверка ответа на запрос получения списка заказов")
def assert_get_orders_response(
        *,
        actual: List[GetOrderResponseSchema],
        expected: List[CreateOrderResponseSchema]
) -> None:
    for order, (actual_order, expected_order) in enumerate(zip(actual, expected)):
        try:
            assert_value(actual_order.id, expected_order.id, f"order[{order}].id")
            assert_value(actual_order.cart_id, expected_order.cart_id, f"order[{order}].cart_id")
            assert_value(actual_order.created_at, expected_order.created_at, f"order[{order}].created_at")
            assert_value(actual_order.user_id, expected_order.user_id, f"order[{order}].user_id")
        except AssertionError as e:
            raise AssertionError(f"Ошибка в элементе {order}: {str(e)}")


@allure.step("Проверка ответа на запрос создания заказа с пустой корзиной")
def assert_empty_cart_order_response(actual: HTTPValidationErrorResponseSchema) -> None:
    assert_value(actual.detail, "Нельзя создать заказ с пустой корзиной", "detail")


@allure.step("Проверка ответа на запрос создания заказа с недоступным продуктом")
def assert_unavailable_product_order_response(actual: HTTPValidationErrorResponseSchema) -> None:
    assert_value(actual.detail, "В корзине есть недоступные для заказа товары", "detail")

