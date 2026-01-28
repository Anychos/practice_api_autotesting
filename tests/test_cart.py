from http import HTTPStatus
from typing import Callable

import allure
import pytest

from clients.cart.client import CartAPIClient
from clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema, DeleteCartItemResponseSchema, \
    UpdateCartItemRequestSchema, UpdateCartItemResponseSchema, DeleteCartResponseSchema, GetCartResponseSchema
from clients.error_shemas import HTTPValidationErrorResponseSchema
from fixtures.cart import CartFixture
from fixtures.product import CreateProductFixture
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.severity import Severity
from tools.allure.story import Story
from tools.assertions.base_assertions import assert_status_code, assert_json_schema
from tools.assertions.cart import assert_add_item_to_cart_response, assert_delete_item_cart_response, \
    assert_update_cart_response, assert_delete_cart_response, \
    assert_not_found_product_response, assert_not_enough_product_response, assert_get_cart_response


@pytest.mark.regression
@pytest.mark.cart
@allure.epic(Epic.USER)
@allure.feature(Feature.CARTS)
class TestCartPositive:
    @pytest.mark.smoke
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Добавление единицы продукта в корзину")
    def test_add_item_to_cart(self,
                              private_cart_client: CartAPIClient,
                              create_available_product: CreateProductFixture
                              ) -> None:
        request = AddItemCartRequestSchema(product_id=create_available_product.product_id)

        response = private_cart_client.add_item_cart_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = AddItemCartResponseSchema.model_validate_json(response.text)
        assert_add_item_to_cart_response(actual=response_data, expected=request)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.story(Story.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Получение данных корзины")
    def test_get_cart(self,
                      private_cart_client: CartAPIClient,
                      create_cart: CartFixture
                      ) -> None:
        response = private_cart_client.get_cart_api()
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetCartResponseSchema.model_validate_json(response.text)
        assert_get_cart_response(actual=response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Удаление единицы продукта из корзины")
    def test_remove_item_from_cart(self,
                                   private_cart_client: CartAPIClient,
                                   create_cart: CartFixture
                                   ) -> None:
        response = private_cart_client.remove_item_cart_api(item_id=create_cart.item_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = DeleteCartItemResponseSchema.model_validate_json(response.text)
        assert_delete_item_cart_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Обновление количества единицы продукта в корзине")
    def test_update_cart(self,
                         private_cart_client: CartAPIClient,
                         create_cart: CartFixture
                         ) -> None:
        request = UpdateCartItemRequestSchema()

        response = private_cart_client.update_cart_item_api(item_id=create_cart.item_id, request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateCartItemResponseSchema.model_validate_json(response.text)
        assert_update_cart_response(actual=response_data, expected=request)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Удаление корзины")
    def test_delete_cart(self,
                         private_cart_client: CartAPIClient,
                         create_cart: CartFixture
                         ) -> None:
        response = private_cart_client.delete_cart_api()
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = DeleteCartResponseSchema.model_validate_json(response.text)
        assert_delete_cart_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())


@pytest.mark.regression
@pytest.mark.cart
@allure.epic(Epic.USER)
@allure.feature(Feature.CARTS)
class TestCartNegative:
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Добавление товара без наличия в корзину")
    def test_add_not_available_product_to_cart(self,
                                               private_cart_client: CartAPIClient,
                                               create_product_factory: Callable[..., CreateProductFixture]
                                               ) -> None:
        product = create_product_factory(is_available=False)
        request = AddItemCartRequestSchema(product_id=product.product_id)

        response = private_cart_client.add_item_cart_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_not_found_product_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Добавление несуществующего товара в корзину")
    def test_add_not_existing_product_to_cart(self, private_cart_client: CartAPIClient) -> None:
        request = AddItemCartRequestSchema(product_id=1001)

        response = private_cart_client.add_item_cart_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_not_found_product_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())

    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Добавление количества одного товара в корзину больше чем доступно")
    def test_add_more_than_available_product_to_cart(self,
                                                     private_cart_client: CartAPIClient,
                                                     create_available_product: CreateProductFixture
                                                     ) -> None:
        request = AddItemCartRequestSchema(product_id=create_available_product.product_id, quantity=2)

        response = private_cart_client.add_item_cart_api(request=request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

        response_data = HTTPValidationErrorResponseSchema.model_validate_json(response.text)
        assert_not_enough_product_response(response_data)
        assert_json_schema(actual=response.json(), schema=response_data.model_json_schema())
