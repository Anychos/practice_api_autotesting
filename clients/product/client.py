import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.authentication.schemas import LoginRequestSchema
from clients.base_client import BaseAPIClient
from clients.private_builder import get_private_client
from clients.product.schemas import CreateProductRequestSchema, CreateProductResponseSchema, UpdateProductRequestSchema
from clients.public_builder import get_public_client
from tools.routes import Routes


class ProductAPIClient(BaseAPIClient):
    @allure.step("Отправка запроса на создание продукта")
    @tracker.track_coverage_httpx(Routes.PRODUCTS)
    def create_product_api(self, request: CreateProductRequestSchema) -> Response:
        return self.post(url=Routes.PRODUCTS, json=request.model_dump())

    def create_product(self, request: CreateProductRequestSchema) -> CreateProductResponseSchema:
        response = self.create_product_api(request)
        return CreateProductResponseSchema.model_validate_json(response.text)

    @allure.step("Отправка запроса на получение продукта")
    @tracker.track_coverage_httpx(f"{Routes.PRODUCTS}/" + "{product_id}")
    def get_product_api(self, product_id: int) -> Response:
        return self.get(url=f"{Routes.PRODUCTS}/{product_id}")

    @allure.step("Отправка запроса на получение списка продуктов")
    @tracker.track_coverage_httpx(Routes.PRODUCTS)
    def get_products_api(self) -> Response:
        return self.get(url=Routes.PRODUCTS)

    @allure.step("Отправка запроса на обновление продукта")
    @tracker.track_coverage_httpx(f"{Routes.PRODUCTS}/" + "{product_id}")
    def update_product_api(self, product_id: int, request: UpdateProductRequestSchema) -> Response:
        return self.put(url=f"{Routes.PRODUCTS}/{product_id}", json=request.model_dump())

    @allure.step("Отправка запроса на удаление продукта")
    @tracker.track_coverage_httpx(f"{Routes.PRODUCTS}/" + "{product_id}")
    def delete_product_api(self, product_id: int) -> Response:
        return self.delete(url=f"{Routes.PRODUCTS}/{product_id}")

def get_public_product_client() -> ProductAPIClient:
    return ProductAPIClient(client=get_public_client())

def get_private_product_client(user: LoginRequestSchema) -> ProductAPIClient:
    return ProductAPIClient(client=get_private_client(user))
