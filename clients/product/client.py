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
    """
    Клиент для работы с API продуктов
    """

    @tracker.track_coverage_httpx(Routes.PRODUCTS)
    @allure.step("Отправка запроса на создание продукта")
    def create_product_api(self,
                           *,
                           request: CreateProductRequestSchema
                           ) -> Response:
        """
        Отправляет запрос на создание продукта

        :param request: Данные для создания продукта
        :return: Ответ сервера с данными созданного продукта
        """

        return self.post(url=Routes.PRODUCTS, json=request.model_dump())

    def create_product(self,
                       *,
                       request: CreateProductRequestSchema
                       ) -> CreateProductResponseSchema:
        response = self.create_product_api(request=request)
        return CreateProductResponseSchema.model_validate_json(response.text)

    @tracker.track_coverage_httpx(f"{Routes.PRODUCTS}/" + "{product_id}")
    @allure.step("Отправка запроса на получение продукта")
    def get_product_api(self,
                        *,
                        product_id: int
                        ) -> Response:
        """
        Отправляет запрос на получение продукта

        :param product_id: Идентификатор продукта
        :return: Ответ сервера с данными продукта
        """

        return self.get(url=f"{Routes.PRODUCTS}/{product_id}")

    @tracker.track_coverage_httpx(Routes.PRODUCTS)
    @allure.step("Отправка запроса на получение списка продуктов")
    def get_products_api(self) -> Response:
        """
        Отправляет запрос на получение списка продуктов

        :return: Ответ сервера со списком продуктов
        """

        return self.get(url=Routes.PRODUCTS)

    @tracker.track_coverage_httpx(f"{Routes.PRODUCTS}/" + "{product_id}")
    @allure.step("Отправка запроса на обновление продукта")
    def update_product_api(self,
                           *,
                           product_id: int,
                           request: UpdateProductRequestSchema
                           ) -> Response:
        """
        Отправляет запрос на обновление продукта

        :param product_id: Идентификатор продукта
        :param request: Данные для обновления продукта
        :return: Ответ сервера с данными обновленного продукта
        """

        return self.put(url=f"{Routes.PRODUCTS}/{product_id}", json=request.model_dump())

    @tracker.track_coverage_httpx(f"{Routes.PRODUCTS}/" + "{product_id}")
    @allure.step("Отправка запроса на удаление продукта")
    def delete_product_api(self,
                           *,
                           product_id: int
                           ) -> Response:
        """
        Отправляет запрос на удаление продукта

        :param product_id: Идентификатор продукта
        :return: Ответ сервера с сообщением об успешном удалении
        """

        return self.delete(url=f"{Routes.PRODUCTS}/{product_id}")


def get_public_product_client() -> ProductAPIClient:
    """
    Создает публичный HTTP клиент для доступа к API продуктов

    :return: Публичный HTTP клиент
    """

    return ProductAPIClient(client=get_public_client())

def get_private_product_client(
        *,
        user: LoginRequestSchema
) -> ProductAPIClient:
    """
    Создает приватный HTTP клиент для доступа к API продуктов

    :param user: Данные пользователя для авторизации
    :return: Приватный HTTP клиент
    """

    return ProductAPIClient(client=get_private_client(user=user))
