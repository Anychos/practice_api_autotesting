from enum import Enum


class Suite(str, Enum):
    AUTHENTICATION = "Authentication"
    USERS = "Users"
    PRODUCTS = "Products"
    CARTS = "Carts"
    ORDERS = "Orders"
