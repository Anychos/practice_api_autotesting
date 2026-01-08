from http import HTTPStatus

import allure
import pytest

from clients.product.client import ProductAPIClient
from clients.product.schemas import CreateProductRequestSchema, CreateProductResponseSchema, GetProductResponseSchema, \
    UpdateProductRequestSchema, UpdateProductResponseSchema, DeleteProductResponseSchema
from fixtures.product import ProductFixture
from tools.assertions.base_assertions import assert_status_code, assert_json_schema
from tools.assertions.product import assert_create_product_response, assert_get_product_response, \
    assert_update_product_response, assert_delete_product_response, assert_get_products_response
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.story import Story
from tools.allure.severity import Severity
from tools.allure.tag import Tag


@pytest.mark.regression
@pytest.mark.product
@allure.feature(Feature.PRODUCTS)
@allure.tag(Tag.PRODUCTS, Tag.REGRESSION)
class TestProductPositive:
    @pytest.mark.smoke
    @allure.epic(Epic.ADMIN)
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_product(self, admin_private_product_client: ProductAPIClient):
        request = CreateProductRequestSchema()

        response = admin_private_product_client.create_product_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = CreateProductResponseSchema.model_validate_json(response.text)
        assert_create_product_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.epic(Epic.USER)
    @allure.story(Story.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_get_product(self, user_private_product_client: ProductAPIClient, create_product: ProductFixture):
        response = user_private_product_client.get_product_api(product_id=create_product.product_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetProductResponseSchema.model_validate_json(response.text)
        assert_get_product_response(response_data, create_product.response)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.smoke
    @allure.epic(Epic.USER)
    @allure.story(Story.GET_ENTITIES)
    @allure.severity(Severity.CRITICAL)
    def test_get_products(self, user_private_product_client: ProductAPIClient, create_product: ProductFixture):
        response = user_private_product_client.get_products_api()
        assert_status_code(response.status_code, HTTPStatus.OK)

        # TODO: add assertions for response

    @allure.epic(Epic.ADMIN)
    @allure.story(Story.UPDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_update_product(self, admin_private_product_client: ProductAPIClient, create_product: ProductFixture):
        request = UpdateProductRequestSchema()

        response = admin_private_product_client.update_product_api(product_id=create_product.product_id, request=request)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateProductResponseSchema.model_validate_json(response.text)
        assert_update_product_response(response_data, request)
        assert_json_schema(response.json(), response_data.model_json_schema())

    @allure.epic(Epic.ADMIN)
    @allure.story(Story.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_delete_product(self, admin_private_product_client: ProductAPIClient, create_product: ProductFixture):
        response = admin_private_product_client.delete_product_api(product_id=create_product.product_id)
        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = DeleteProductResponseSchema.model_validate_json(response.text)
        assert_delete_product_response(response_data)
        assert_json_schema(response.json(), response_data.model_json_schema())

@pytest.mark.regression
@pytest.mark.product
@allure.feature(Feature.PRODUCTS)
@allure.tag(Tag.PRODUCTS, Tag.REGRESSION)
class TestProductNegative:
    @allure.epic(Epic.ADMIN)
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_product_wrong_data_format(self):
        pass

    @allure.epic(Epic.ADMIN)
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_product_without_required_field(self):
        pass

    @allure.epic(Epic.ADMIN)
    @allure.story(Story.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_product_empty_data(self):
        pass
