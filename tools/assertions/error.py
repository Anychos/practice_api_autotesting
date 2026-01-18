from clients.error_shemas import InputValidationErrorResponseSchema, HTTPValidationErrorResponseSchema, ErrorSchema
from tools.assertions.base_assertions import assert_value, assert_length


def assert_error(
        actual: ErrorSchema,
        expected: ErrorSchema
) -> None:
    assert_value(actual.type, expected.type, "type")
    assert_value(actual.location, expected.location, "location")
    assert_value(actual.message, expected.message, "message")
    assert_value(actual.input, expected.input, "input")
    assert_value(actual.context, expected.context, "reason")


def assert_input_validation_error_response(
        *,
        actual: InputValidationErrorResponseSchema,
        expected: InputValidationErrorResponseSchema
) -> None:
    assert_length(actual.detail, expected.detail, "detail")

    for index, expected_error in enumerate(expected.detail):
        assert_error(actual=actual.detail[index], expected=expected_error)


def assert_http_validation_error_response(
        *,
        actual: HTTPValidationErrorResponseSchema,
        expected: HTTPValidationErrorResponseSchema
) -> None:
    assert_value(actual.detail, expected.detail, "detail")
