from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

from api.models.bancard import (
    BANCARD_STATUS_ERROR,
    BANCARD_LEVEL_ERROR,
    BANCARD_CODE_NOT_AUTHORIZED,
    BANCARD_CODE_FORBIDDEN,
    BANCARD_CODE_UNKNOWN_ERROR,
)


async def http_exception_handler(req: Request, exc: HTTPException):
    tid = int(req.query_params.get("tid", "0"))
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        response_data = {
            "status":
                BANCARD_STATUS_ERROR,
            "tid":
                tid,
            "messages":
                [
                    {
                        "level": BANCARD_LEVEL_ERROR,
                        "key": BANCARD_CODE_NOT_AUTHORIZED,
                        "dsc": ["No autorizado"]
                    }
                ]
        }

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        response_data = {
            "status":
                BANCARD_STATUS_ERROR,
            "tid":
                tid,
            "messages":
                [
                    {
                        "level": BANCARD_LEVEL_ERROR,
                        "key": BANCARD_CODE_FORBIDDEN,
                        "dsc": ["Prohibido"]
                    }
                ]
        }

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    raise


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
