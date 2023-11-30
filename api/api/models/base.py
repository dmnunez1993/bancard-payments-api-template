from typing import Any, TypeVar

from pydantic import BaseModel as CoreBaseModel, ValidationError
from pydantic_async_validation import AsyncValidationModelMixin
from pydantic_core import InitErrorDetails, PydanticCustomError

Model = TypeVar('Model', bound='CoreBaseModel')


class BaseModel(AsyncValidationModelMixin, CoreBaseModel):
    @classmethod
    async def async_validate(
        cls: type[Model],
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None
    ):
        instance_unverified = cls.model_construct(**obj)
        line_errors = []

        try:
            instance = cls.model_validate(
                obj,
                strict=strict,
                from_attributes=from_attributes,
                context=context
            )
        except ValidationError as exc:
            for error in exc.errors():
                error["type"] = PydanticCustomError(error["type"], error["msg"])
                line_errors.append(InitErrorDetails(**error))

        instance_unverified = cls.model_construct(**obj)
        try:
            await instance_unverified.model_async_validate()
        except ValidationError as exc:
            for error in exc.errors():
                error["type"] = PydanticCustomError(error["type"], error["msg"])
                line_errors.append(InitErrorDetails(**error))

        if len(line_errors) > 0:
            raise ValidationError.from_exception_data(cls.__name__, line_errors)

        return instance

    class Config:
        populate_by_name = True
