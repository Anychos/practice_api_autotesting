from typing import List

from pydantic import BaseModel, Field, ConfigDict


class ErrorSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str
    location: List[str | int] = Field(alias="loc")
    message: str = Field(alias="msg")

class ContextSchema(BaseModel):
    reason: str

class ValidationErrorSchema(ErrorSchema):
    model_config = ConfigDict(populate_by_name=True)

    input: str
    context: ContextSchema = Field(alias="ctx")

class ValidationErrorResponseSchema(BaseModel):
    detail: List[ValidationErrorSchema]

class HTTPValidationErrorResponseSchema(BaseModel):
    detail: List[ErrorSchema]
