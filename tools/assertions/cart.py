import allure

from clients.cart.schemas import AddItemCartResponseSchema, AddItemCartRequestSchema, DeleteCartResponseSchema, \
    DeleteCartItemResponseSchema, UpdateCartItemResponseSchema, UpdateCartItemRequestSchema
from clients.error_shemas import HTTPValidationErrorResponseSchema
from tools.assertions.base_assertions import assert_value, assert_field_exists


@allure.step("Проверка ответа на запрос добавления продукта в корзину")
def assert_add_item_to_cart_response(actual: AddItemCartResponseSchema, expected: AddItemCartRequestSchema) -> None:
    assert_field_exists(actual.product_id, "item_id")
    assert_value(actual.product_id, expected.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")


@allure.step("Проверка ответа на запрос получения корзины")
def assert_get_cart_response():
    pass


@allure.step("Проверка ответа на запрос обновления продукта в корзине")
def assert_update_cart_response(actual: UpdateCartItemResponseSchema, expected: UpdateCartItemRequestSchema) -> None:
    assert_field_exists(actual.product_id, "item_id")
    assert_field_exists(actual.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")


@allure.step("Проверка ответа на запрос удаления корзины")
def assert_delete_cart_response(actual: DeleteCartResponseSchema) -> None:
    assert_value(actual.message, "Корзина очищена", "message")


@allure.step("Проверка ответа на запрос удаления продукта из корзины")
def assert_delete_item_cart_response(actual: DeleteCartItemResponseSchema) -> None:
    assert_value(actual.message, "Продукт удален из корзины", "message")


@allure.step("Проверка ответа на запрос с добавлением несуществующего продукта в корзину")
def assert_not_found_product_response(actual: HTTPValidationErrorResponseSchema) -> None:
    assert_value(actual.detail, "Продукт не найден или недоступен", "detail")


@allure.step("Проверка ответа на запрос с добавлением в корзину больше чем имеется продукта")
def assert_not_enough_product_response(actual: HTTPValidationErrorResponseSchema) -> None:
    assert_value(actual.detail, "Недостаточно товара в наличии", "detail")

