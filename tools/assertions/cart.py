import allure

from clients.cart.schemas import AddItemCartResponseSchema, AddItemCartRequestSchema, DeleteCartResponseSchema, \
    DeleteCartItemResponseSchema, UpdateCartItemResponseSchema, UpdateCartItemRequestSchema, GetCartResponseSchema
from clients.error_shemas import HTTPValidationErrorResponseSchema
from tools.assertions.base_assertions import assert_value, assert_field_exists
from tools.assertions.error import assert_http_validation_error_response


@allure.step("Проверка ответа на запрос добавления продукта в корзину")
def assert_add_item_to_cart_response(
        *,
        actual: AddItemCartResponseSchema,
        expected: AddItemCartRequestSchema
) -> None:
    assert_field_exists(actual.product_id, "item_id")
    assert_value(actual.product_id, expected.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")


def assert_product_in_cart(actual: GetCartResponseSchema, index: int):
    assert_value(actual.items[index].product_id, actual.items[index].product_id, "product_id")
    assert_value(actual.items[index].quantity, actual.items[index].quantity, "quantity")
    assert_value(actual.items[index].product_name, actual.items[index].product_name, "price")
    assert_value(actual.items[index].product_price, actual.items[index].product_price, "product_price")
    assert_value(actual.items[index].product_image_url, actual.items[index].product_image_url, "product_image_url")
    assert_value(actual.items[index].is_available, actual.items[index].is_available, "is_available")
    assert_value(actual.items[index].has_enough_stock, actual.items[index].has_enough_stock, "has_enough_stock")
    assert_value(actual.items[index].available_quantity, actual.items[index].available_quantity, "available_quantity")


@allure.step("Проверка ответа на запрос получения корзины")
def assert_get_cart_response(actual: GetCartResponseSchema):
    assert_field_exists(actual.id, "id")
    assert_field_exists(actual.user_id, "user_id")
    assert_field_exists(actual.total_quantity, "total_quantity")
    assert_field_exists(actual.total_price, "total_price")
    assert_field_exists(actual.items, "items")

    assert_product_in_cart(actual, 0)


@allure.step("Проверка ответа на запрос обновления продукта в корзине")
def assert_update_cart_response(
        *,
        actual: UpdateCartItemResponseSchema,
        expected: UpdateCartItemRequestSchema
) -> None:
    assert_field_exists(actual.product_id, "item_id")
    assert_field_exists(actual.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")


@allure.step("Проверка ответа на запрос удаления корзины")
def assert_delete_cart_response(actual: DeleteCartResponseSchema) -> None:
    expected = DeleteCartResponseSchema(
        message="Корзина очищена"
    )
    assert_value(actual.message, expected.message, "message")


@allure.step("Проверка ответа на запрос удаления продукта из корзины")
def assert_delete_item_cart_response(actual: DeleteCartItemResponseSchema) -> None:
    expected = DeleteCartItemResponseSchema(
        message="Продукт удален из корзины"
    )
    assert_value(actual.message, expected.message, "message")


@allure.step("Проверка ответа на запрос с добавлением несуществующего продукта в корзину")
def assert_not_found_product_response(actual: HTTPValidationErrorResponseSchema) -> None:
    expected = HTTPValidationErrorResponseSchema(
        detail="Продукт не найден или недоступен"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)


@allure.step("Проверка ответа на запрос с добавлением в корзину больше чем имеется продукта")
def assert_not_enough_product_response(actual: HTTPValidationErrorResponseSchema) -> None:
    expected = HTTPValidationErrorResponseSchema(
        detail="Недостаточно товара в наличии"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)

