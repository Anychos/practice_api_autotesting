import allure
import pytest

from clients.order.client import OrderAPIClient
from clients.order.schemas import CreateOrderRequestSchema
from fixtures.cart import CartFixture
from tools.allure.epic import Epic
from tools.allure.feature import Feature
from tools.allure.parent_suite import ParentSuite
from tools.allure.severity import Severity
from tools.allure.story import Story
from tools.allure.sub_suite import SubSuite
from tools.allure.suite import Suite
from tools.allure.tag import Tag


@pytest.mark.regression
@pytest.mark.cart
@allure.epic(Epic.USER_FRONTEND)
@allure.feature(Feature.CARTS)
@allure.parent_suite(ParentSuite.USER_FRONTEND)
@allure.suite(Suite.CARTS)
@allure.tag(Tag.CARTS, Tag.REGRESSION)
class TestOrder:
    @pytest.mark.smoke
    @allure.story(Story.CREATE_ENTITY)
    @allure.sub_suite(SubSuite.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_order(self, private_order_client: OrderAPIClient, create_cart: CartFixture):
        request = CreateOrderRequestSchema(cart_id=create_cart.response.id)
