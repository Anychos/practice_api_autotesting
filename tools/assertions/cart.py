from typing import List

from clients.cart.schemas import AddItemCartResponseSchema, AddItemCartRequestSchema, GetCartResponseSchema, \
    DeleteCartResponseSchema, DeleteCartItemResponseSchema, UpdateCartItemResponseSchema, UpdateCartItemRequestSchema
from tools.assertions.base_assertions import assert_value, assert_field_exists, assert_length


def assert_add_item_to_cart_response(actual: AddItemCartResponseSchema, expected: AddItemCartRequestSchema) -> None:
    assert_field_exists(actual.id, "item_id")
    assert_value(actual.product_id, expected.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")

def assert_get_cart_response(actual: GetCartResponseSchema,
                             expected: List[AddItemCartResponseSchema]) -> None:
    assert_field_exists(actual.id, "cart_id")
    assert_field_exists(actual.user_id, "user_id")
    assert_field_exists(actual.total_quantity, "total_quantity")
    assert_field_exists(actual.items, "items_list")

    assert_length(actual.items, expected, "items_list")

    for item, (actual_item, expected_item) in enumerate(zip(actual.items, expected)):
        try:
            assert_value(actual_item.id, expected_item.id, f"items[{item}].id")
            assert_value(actual_item.product_id, expected_item.product_id, f"items[{item}].product_id")
            assert_value(actual_item.quantity, expected_item.quantity, f"items[{item}].quantity")
        except AssertionError as e:
            raise AssertionError(f"Ошибка в элементе {item}: {str(e)}")

    calculated_total = sum(item.quantity for item in actual.items)
    assert actual.total_quantity == calculated_total, \
        f"total_quantity должен быть {calculated_total}, получено: {actual.total_quantity}"

def assert_update_cart_response(actual: UpdateCartItemResponseSchema, expected: UpdateCartItemRequestSchema) -> None:
    assert_field_exists(actual.id, "item_id")
    assert_field_exists(actual.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")

def assert_delete_cart_response(actual: DeleteCartResponseSchema) -> None:
    assert_value(actual.message, "Cart cleared successfully", "message")

def assert_delete_item_cart_response(actual: DeleteCartItemResponseSchema) -> None:
    assert_value(actual.message, "Item removed from cart successfully", "message")

