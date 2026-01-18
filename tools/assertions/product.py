from typing import Any, List

import allure

from clients.error_shemas import InputValidationErrorResponseSchema
from clients.product.schemas import CreateProductResponseSchema, CreateProductRequestSchema, ProductSchema, \
    GetProductResponseSchema, UpdateProductResponseSchema, FullUpdateProductRequestSchema, DeleteProductResponseSchema, \
    PartialUpdateProductRequestSchema
from tools.assertions.base_assertions import assert_field_exists, assert_value


@allure.step("Проверка данных продукта по схеме")
def assert_product(
        actual: ProductSchema,
        expected: ProductSchema
) -> None:
    assert_value(actual.name, expected.name, "name")
    assert_value(actual.description, expected.description, "description")
    assert_value(actual.price, expected.price, "price")
    assert_value(actual.is_available, expected.is_available, "is_available")
    assert_value(actual.image_url, expected.image_url, "image_url")
    assert_value(actual.stock_quantity, expected.stock_quantity, "stock_quantity")


@allure.step("Проверка ответа на запрос создания продукта")
def assert_create_product_response(
        *,
        actual: CreateProductResponseSchema,
        expected: CreateProductRequestSchema
) -> None:
    assert_field_exists(actual.id, "id")
    assert_product(actual, expected)


@allure.step("Проверка ответа на запрос получения продукта")
def assert_get_product_response(
        *,
        actual: GetProductResponseSchema,
        expected: CreateProductResponseSchema
) -> None:
    assert_value(actual.id, expected.id, "id")
    assert_product(actual, expected)


@allure.step("Проверка ответа на запрос списка продуктов")
def assert_get_products_response(
        *,
        get_products_response: List[GetProductResponseSchema],
        create_product_responses: List[CreateProductResponseSchema]
) -> None:
    for index, create_product_response in enumerate(create_product_responses):
        assert_product(get_products_response[index], create_product_response)


@allure.step("Проверка ответа на запрос полного обновления продукта")
def assert_full_update_product_response(
        *,
        actual: UpdateProductResponseSchema,
        expected: FullUpdateProductRequestSchema
) -> None:
    assert_field_exists(actual.id, "id")
    assert_product(actual, expected)


@allure.step("Проверка ответа на запрос частичного обновления продукта")
def assert_partial_update_product_response(
        *,
        actual: UpdateProductResponseSchema,
        expected: PartialUpdateProductRequestSchema
) -> None:
    expected_data = expected.model_dump(exclude_none=True)

    for field, expected_value in expected_data.items():
        actual_value = getattr(actual, field)
        assert_value(actual_value, expected_value, field)


@allure.step("Проверка ответа на запрос удаления продукта")
def assert_delete_product_response(actual: DeleteProductResponseSchema) -> None:
    assert_value(actual.message, "Продукт удален", "message")


@allure.step("Проверка ответа на запрос создания продукта с некорректным форматом в данных")
def assert_wrong_data_format_response(
        *,
        actual: InputValidationErrorResponseSchema,
        wrong_field: str,
        wrong_value: Any
) -> None:
    error_messages = [
        "Input should be a valid string",
        "Input should be a valid number, unable to parse string as a number"
    ]

    assert actual.detail, "Список ошибок пуст"
    assert len(actual.detail) == 1, "В ответе более одной ошибки"

    error = actual.detail[0]

    assert error.type in ["string_type", "float_parsing"]
    assert error.location == ["body", wrong_field]
    assert any(message in error.message for message in error_messages), (
        f"Неожиданная ошибка: {error.message}"
    )
    assert error.input == wrong_value


@allure.step("Проверка ответа на запрос создания продукта с пустым обязательным полем")
def assert_empty_required_field_response(
        *,
        actual: InputValidationErrorResponseSchema,
        wrong_field: str,
        wrong_value: Any
) -> None:
    error_messages = [
        "String should have at least 2 characters",
        "String should have at least 10 characters",
        "Input should be greater than 0",
        "Value error, URL изображения не может быть пустым"
    ]
    error_types = [
        "string_too_short",
        "string_too_long",
        "greater_than",
        "value_error"
    ]

    assert actual.detail, "Список ошибок пуст"
    assert len(actual.detail) == 1, "В ответе более одной ошибки"

    error = actual.detail[0]

    assert error.type in error_types
    assert error.location == ["body", wrong_field]
    assert any(message in error.message for message in error_messages), (
        f"Неожиданная ошибка: {error.message}"
    )
    assert error.input == wrong_value
    assert error.context, "Контекст ошибки пуст"

@allure.step("Проверка ответа на запрос создания продукта с некорректным URL изображения")
def assert_invalid_image_url_response():
    pass
