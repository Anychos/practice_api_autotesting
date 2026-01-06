from enum import Enum


class Routes(str, Enum):
    LOGIN = "/login"
    USERS = "/users"
    PRODUCTS = "/products"
    CARTS = "/cart"
    ORDERS = "/orders"

    def __str__(self):
        return self.value
