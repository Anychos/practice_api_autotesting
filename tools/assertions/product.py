import allure

from clients.product.schemas import CreateProductResponseSchema, CreateProductRequestSchema, ProductSchema, \
    GetProductResponseSchema, UpdateProductResponseSchema, UpdateProductRequestSchema, DeleteProductResponseSchema
from tools.assertions.base_assertions import assert_field_exists, assert_value


@allure.step("Проверка данных продукта по схеме")
def assert_product(actual: ProductSchema, expected: ProductSchema) -> None:
    assert_value(actual.name, expected.name, "name")
    assert_value(actual.description, expected.description, "description")
    assert_value(actual.price, expected.price, "price")
    assert_value(actual.is_available, expected.is_available, "is_available")
    assert_value(actual.image_url, expected.image_url, "image_url")

@allure.step("Проверка ответа на запрос создания продукта")
def assert_create_product_response(actual: CreateProductResponseSchema, expected: CreateProductRequestSchema) -> None:
    assert_field_exists(actual.id, "id")
    assert_product(actual, expected)

@allure.step("Проверка ответа на запрос получения продукта")
def assert_get_product_response(actual: GetProductResponseSchema, expected: CreateProductResponseSchema) -> None:
    assert_value(actual.id, expected.id, "id")
    assert_product(actual, expected)

@allure.step("Проверка ответа на запрос списка продуктов")
def assert_get_products_response(
        get_products_response: list[GetProductResponseSchema],
        create_product_responses: list[CreateProductResponseSchema]
) -> None:
    for index, create_product_response in enumerate(create_product_responses):
        assert_product(get_products_response[index], create_product_response)

@allure.step("Проверка ответа на запрос обновления продукта")
def assert_update_product_response(actual: UpdateProductResponseSchema, expected: UpdateProductRequestSchema) -> None:
    assert_field_exists(actual.id, "id")
    assert_product(actual, expected)

@allure.step("Проверка ответа на запрос удаления продукта")
def assert_delete_product_response(actual: DeleteProductResponseSchema) -> None:
    assert_value(actual.message, "Product deleted successfully", "message")
