from clients.error_shemas import InputValidationErrorResponseSchema, HTTPValidationErrorResponseSchema, \
    InputValidationErrorSchema, ErrorSchema
from tools.assertions.base_assertions import assert_value, assert_length


def assert_error(actual: ErrorSchema, expected: ErrorSchema) -> None:
    assert_value(actual.message, expected.message, "message")
    assert_value(actual.type, expected.type, "type")
    assert_value(actual.location, expected.location, "location")

def assert_input_validation_error(actual: InputValidationErrorSchema, expected: InputValidationErrorSchema) -> None:
    assert_error(actual, expected)
    assert_value(actual.input, expected.input, "input")
    assert_value(actual.context, expected.context, "reason")

def assert_input_validation_error_response(actual: InputValidationErrorResponseSchema, expected: InputValidationErrorResponseSchema) -> None:
    assert_length(actual.detail, expected.detail, "detail")

    for error, detail in enumerate(expected.detail):
        assert_input_validation_error(actual.detail[error], detail)

def assert_http_validation_error_response(actual: HTTPValidationErrorResponseSchema, expected: HTTPValidationErrorResponseSchema) -> None:
    assert_value(actual.detail, expected.detail, "detail")
