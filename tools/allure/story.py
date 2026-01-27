from enum import Enum


class Story(str, Enum):
    LOGIN = "Login"
    REGISTRATION = "Registration"

    GET_ENTITY = "Get entity"
    GET_ENTITIES = "Get entities"
    CREATE_ENTITY = "Create entity"
    UPDATE_ENTITY = "Update entity"
    DELETE_ENTITY = "Delete entity"
