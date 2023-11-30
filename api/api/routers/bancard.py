from typing import Annotated

from fastapi import Response, status, Query

from api.common.router import create_api_router
from api.models.bancard import (
    InvoicesResponse,
    BANCARD_STATUS_SUCCESS,
    BANCARD_LEVEL_INFO,
    BANCARD_LEVEL_SUCCESS,
    BANCARD_CODE_SUBSCRIBER_NOT_FOUND,
    BANCARD_CODE_SUBSCRIBER_WITHOUT_DEBT,
    BANCARD_CODE_QUERY_PROCESSED,
)

from database.connection import db
from database.models.invoice_request import invoice_requests

from template_data.invoices import (subscriber_exists, get_subscriber_invoices)

router = create_api_router()


@router.get("/invoices", response_model=InvoicesResponse)
async def get_invoices(
    tid: int,
    prd_id: int,
    response: Response,
    addl: str | None = None,
    sub_id: Annotated[list, Query(alias="sub_id[]")] = [],
):
    request_data = {
        "tid": tid,
        "prd_id": prd_id,
        "sub_ids": sub_id,
        "addl": addl
    }

    if not subscriber_exists(sub_id):
        request_data["response_code"] = status.HTTP_404_NOT_FOUND
        query = invoice_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = status.HTTP_404_NOT_FOUND

        return {
            "status":
                BANCARD_STATUS_SUCCESS,
            "tid":
                tid,
            "messages":
                [
                    {
                        "level": BANCARD_LEVEL_INFO,
                        "key": BANCARD_CODE_SUBSCRIBER_NOT_FOUND,
                        "dsc": ["El abonado no existe"]
                    },
                ]
        }

    invoices = get_subscriber_invoices(sub_id)

    if len(invoices) == 0:
        request_data["response_code"] = status.HTTP_403_FORBIDDEN
        query = invoice_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = status.HTTP_403_FORBIDDEN

        return {
            "status":
                BANCARD_STATUS_SUCCESS,
            "tid":
                tid,
            "messages":
                [
                    {
                        "level":
                            BANCARD_LEVEL_INFO,
                        "key":
                            BANCARD_CODE_SUBSCRIBER_WITHOUT_DEBT,
                        "dsc":
                            [
                                "No se encontraron pagos pendientes para el cliente"
                            ]
                    },
                ]
        }

    response.status_code = status.HTTP_200_OK

    request_data["response_code"] = status.HTTP_200_OK
    query = invoice_requests.insert().values(request_data)
    await db.execute(query)

    print(invoices)

    return {
        "status": BANCARD_STATUS_SUCCESS,
        "tid": tid,
        "messages":
            [
                {
                    "level": BANCARD_LEVEL_SUCCESS,
                    "key": BANCARD_CODE_QUERY_PROCESSED,
                    "dsc": ["Consulta procesada con éxito"]
                }
            ],
        "invoices": invoices
    }
