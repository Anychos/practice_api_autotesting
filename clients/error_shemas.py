from typing import List, Any

from pydantic import BaseModel, Field, ConfigDict


class ErrorSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str
    location: List[str | int] = Field(alias="loc")
    message: str = Field(alias="msg")
    input: Any | None = Field(default=None)
    context: dict[str, Any] | None = Field(alias="ctx", default=None)


class InputValidationErrorResponseSchema(BaseModel):
    detail: List[ErrorSchema]


class HTTPValidationErrorResponseSchema(BaseModel):
    detail: str
