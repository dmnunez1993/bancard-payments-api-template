from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from api.common.status import ERROR, FIELD_ERRORS


def _get_field_errors(errors):
    field_errors = {}
    current_errors = field_errors
    for error in errors:
        if error['type'] != "missing" and error['type'] != "value_error":
            continue
        for idx in range(0, len(error['loc'])):
            value = error['loc'][idx]
            if isinstance(value, int) or value == "body":
                continue

            if idx + 1 < len(error['loc']):
                next_value = error['loc'][idx + 1]

                if isinstance(next_value, int):
                    if value not in current_errors:
                        current_errors[value] = []

                    while len(current_errors[value]) <= next_value:
                        current_errors[value].append({})

                else:
                    current_errors[value] = {}
            else:
                if value not in current_errors:
                    current_errors[value] = []
                current_errors[value].append(error['msg'])
                break

        current_errors = field_errors

    return field_errors


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    errors = exc.errors()
    response_data = {
        "status":
            "success",
        "tid":
            0,
        "messages":
            [
                {
                    "level": "info",
                    "key": "InvalidParameters",
                    "dsc": ["Consulta inválida"]
                }
            ]
    }
    for error in errors:
        if error['type'] == 'value_error.jsondecode':
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    return JSONResponse(
        content=response_data, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


async def pydantic_exception_handler(req: Request, exc: ValidationError):
    return await validation_exception_handler(
        req, RequestValidationError(errors=exc.errors())
    )
