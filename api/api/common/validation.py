from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from api.models.bancard import (
    BANCARD_STATUS_ERROR,
    BANCARD_LEVEL_ERROR,
    BANCARD_CODE_INVALID_PARAMETERS,
    BANCARD_CODE_MISSING_PARAMETER,
    BANCARD_CODE_UNKNOWN_ERROR,
)


def _get_field_messages(errors):
    messages = []
    for error in errors:
        if error['type'] != "missing" and error['type'] != "value_error":
            continue

        key = BANCARD_CODE_MISSING_PARAMETER if error[
            'type'] == "missing" else BANCARD_CODE_INVALID_PARAMETERS
        for idx in range(0, len(error['loc'])):
            value = error['loc'][idx]
            if isinstance(value, int) or value == "body" or value == "query":
                continue

            messages.append(
                {
                    "level": BANCARD_LEVEL_ERROR,
                    "key": key,
                    "dsc": [f"Campo requerido en solicitud: {value}"]
                }
            )

    return messages


async def validation_exception_handler(
    req: Request, exc: RequestValidationError
):
    tid = int(req.query_params.get("tid", "0"))
    errors = exc.errors()
    for error in errors:
        if error['type'] == 'value_error.jsondecode' or error[
            "type"] == 'json_invalid':
            response_data = {
                "status":
                    BANCARD_STATUS_ERROR,
                "tid":
                    tid,
                "messages":
                    [
                        {
                            "level": BANCARD_LEVEL_ERROR,
                            "key": BANCARD_CODE_INVALID_PARAMETERS,
                            "dsc": ["Solicitud Inválida"]
                        }
                    ]
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    messages = _get_field_messages(errors)

    response_data = {
        "status": BANCARD_STATUS_ERROR,
        "tid": tid,
        "messages": messages
    }

    return JSONResponse(
        content=response_data, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


async def pydantic_exception_handler(req: Request, exc: ValidationError):
    return await validation_exception_handler(
        req, RequestValidationError(errors=exc.errors())
    )


async def global_exception_handler(req: Request, _: Exception):
    tid = int(req.query_params.get("tid", "0"))
    response_data = {
        "status":
            BANCARD_STATUS_ERROR,
        "tid":
            tid,
        "messages":
            [
                {
                    "level": BANCARD_LEVEL_ERROR,
                    "key": BANCARD_CODE_UNKNOWN_ERROR,
                    "dsc": ["Error desconocido"]
                }
            ]
    }

    return JSONResponse(
        content=response_data,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
