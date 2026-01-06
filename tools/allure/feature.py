from enum import Enum


class Feature(str, Enum):
    AUTHENTICATION = "Authentication"
    USERS = "Users"
    PRODUCTS = "Products"
    CARTS = "Carts"
    ORDERS = "Orders"
