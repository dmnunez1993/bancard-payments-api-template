import json
from typing import Annotated

from fastapi import Response, status, Query

from api.common.router import create_api_router
from api.models.bancard import (
    BancardResponse,
    InvoicesResponse,
    PaymentRequest,
    PaymentSuccessfulResponse,
    ReversalRequest,
    BANCARD_STATUS_SUCCESS,
    BANCARD_STATUS_ERROR,
    BANCARD_LEVEL_INFO,
    BANCARD_LEVEL_SUCCESS,
    BANCARD_LEVEL_ERROR,
    BANCARD_CODE_SUBSCRIBER_NOT_FOUND,
    BANCARD_CODE_SUBSCRIBER_WITHOUT_DEBT,
    BANCARD_CODE_PAYMENT_NOT_AUTHORIZED,
    BANCARD_CODE_PAYMENT_PROCESSED,
    BANCARD_CODE_QUERY_PROCESSED,
    BANCARD_CODE_TRANSACTION_NOT_REVERSED,
    BANCARD_CODE_TRANSACTION_REVERSED,
)

from database.connection import db
from database.models.invoice_request import invoice_requests
from database.models.payment_request import payment_requests
from database.models.reverse_payment_request import reverse_payment_requests

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
        request_data["status"] = BANCARD_STATUS_SUCCESS
        request_data["level"] = BANCARD_LEVEL_INFO
        request_data["key"] = BANCARD_CODE_SUBSCRIBER_NOT_FOUND
        request_data["dsc"] = ["El abonado no existe"]
        query = invoice_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"]
                    },
                ]
        }

    invoices = get_subscriber_invoices(sub_id)

    if len(invoices) == 0:
        request_data["response_code"] = status.HTTP_403_FORBIDDEN
        request_data["status"] = BANCARD_STATUS_SUCCESS
        request_data["level"] = BANCARD_LEVEL_INFO
        request_data["key"] = BANCARD_CODE_SUBSCRIBER_WITHOUT_DEBT
        request_data["dsc"] = [
            "No se encontraron pagos pendientes para el cliente"
        ]

        query = invoice_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"],
                    },
                ]
        }

    request_data["response_code"] = status.HTTP_200_OK
    request_data["status"] = BANCARD_STATUS_SUCCESS
    request_data["level"] = BANCARD_LEVEL_SUCCESS
    request_data["key"] = BANCARD_CODE_QUERY_PROCESSED
    request_data["dsc"] = ["Consulta procesada con éxito"]
    query = invoice_requests.insert().values(request_data)
    await db.execute(query)

    response.status_code = request_data["response_code"]

    return {
        "status": request_data["status"],
        "tid": tid,
        "messages":
            [
                {
                    "level": request_data["level"],
                    "key": request_data["key"],
                    "dsc": request_data["dsc"]
                }
            ],
        "invoices": invoices
    }


@router.post("/payment", response_model=PaymentSuccessfulResponse)
async def payment(payment_request: PaymentRequest, response: Response):
    request_data = {
        "tid": payment_request.tid,
        "sub_ids": payment_request.sub_id,
        "inv_ids": payment_request.inv_id,
        "amt": payment_request.amt,
        "curr": payment_request.curr,
        "trn_dat": payment_request.trn_dat,
        "trn_hou": payment_request.trn_hou,
        "cm_amt": payment_request.cm_amt,
        "cm_curr": payment_request.cm_curr,
        "addl": json.dumps(payment_request.addl.model_dump()),
        "type": payment_request.type
    }

    if not subscriber_exists(payment_request.sub_id):
        request_data["response_code"] = status.HTTP_404_NOT_FOUND
        request_data["status"] = BANCARD_STATUS_SUCCESS
        request_data["level"] = BANCARD_LEVEL_INFO
        request_data["key"] = BANCARD_CODE_SUBSCRIBER_NOT_FOUND
        request_data["dsc"] = ["El abonado no existe"]
        query = payment_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"]
                    },
                ]
        }

    invoices = get_subscriber_invoices(
        payment_request.sub_id,
        payment_request.inv_id,
    )

    if len(invoices) == 0:
        request_data["response_code"] = status.HTTP_403_FORBIDDEN
        request_data["status"] = BANCARD_STATUS_SUCCESS
        request_data["level"] = BANCARD_LEVEL_INFO
        request_data["key"] = BANCARD_CODE_SUBSCRIBER_WITHOUT_DEBT
        request_data["dsc"] = [
            "El pago no fue aprobado. El abonado no tiene deuda pendiente"
        ]

        query = payment_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"],
                    },
                ]
        }

    total = 0

    if len(invoices) < len(payment_request.inv_id):
        request_data["response_code"] = status.HTTP_403_FORBIDDEN
        request_data["status"] = BANCARD_STATUS_SUCCESS
        request_data["level"] = BANCARD_LEVEL_INFO
        request_data["key"] = BANCARD_CODE_PAYMENT_NOT_AUTHORIZED
        request_data["dsc"] = [
            "El pago no fue aprobado. No se econtraron todas las facturas solicitadas"
        ]

        query = payment_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"],
                    },
                ]
        }

    for invoice in invoices:
        total += invoice["amt"]

    if payment_request.amt < total:
        request_data["response_code"] = status.HTTP_403_FORBIDDEN
        request_data["status"] = BANCARD_STATUS_SUCCESS
        request_data["level"] = BANCARD_LEVEL_INFO
        request_data["key"] = BANCARD_CODE_PAYMENT_NOT_AUTHORIZED
        request_data["dsc"] = [
            "El pago no fue aprobado. Los montos no equivalen a la suma del total"
        ]

        query = payment_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"],
                    },
                ]
        }

    request_data["tkt"] = 0
    request_data["aut_cod"] = 0
    request_data["response_code"] = status.HTTP_200_OK
    request_data["status"] = BANCARD_STATUS_SUCCESS
    request_data["level"] = BANCARD_LEVEL_SUCCESS
    request_data["key"] = BANCARD_CODE_PAYMENT_PROCESSED
    request_data["dsc"] = ["El pago fue autorizado"]
    query = payment_requests.insert().values(request_data)
    await db.execute(query)

    response.status_code = request_data["response_code"]

    return {
        "status": request_data["status"],
        "tid": request_data["tid"],
        "tkt": request_data["tkt"],
        "aut_cod": request_data["aut_cod"],
        "messages":
            [
                {
                    "level": request_data["level"],
                    "key": request_data["key"],
                    "dsc": request_data["dsc"]
                }
            ],
        "prnt_msg": [],
    }


@router.post("/payment", response_model=BancardResponse)
async def reverse(reversal_request: ReversalRequest, response: Response):
    request_data = {
        "tid": reversal_request.tid,
    }

    reversal_query = reverse_payment_requests.select(
        reverse_payment_requests.c.tid == request_data["tid"]
    )

    reversal_res = await db.fetch_one(reversal_query)

    if reversal_res is not None:
        request_data["response_code"] = status.HTTP_403_FORBIDDEN
        request_data["status"] = BANCARD_STATUS_ERROR
        request_data["level"] = BANCARD_LEVEL_ERROR
        request_data["key"] = BANCARD_CODE_TRANSACTION_NOT_REVERSED
        request_data["dsc"] = ["Este pago ya fue revertido"]

        query = reverse_payment_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"],
                    },
                ]
        }

    payments_query = payment_requests.select(
        payment_requests.c.tid == request_data["tid"],
        payment_requests.c.code == BANCARD_CODE_PAYMENT_PROCESSED
    )

    payments_res = await db.fetch_one(payments_query)

    if payments_res is None:
        request_data["response_code"] = status.HTTP_403_FORBIDDEN
        request_data["status"] = BANCARD_STATUS_ERROR
        request_data["level"] = BANCARD_LEVEL_ERROR
        request_data["key"] = BANCARD_CODE_TRANSACTION_NOT_REVERSED
        request_data["dsc"] = ["Reversión no aprobada. No existe el pago"]

        query = reverse_payment_requests.insert().values(request_data)
        await db.execute(query)

        response.status_code = request_data["response_code"]

        return {
            "status":
                request_data["status"],
            "tid":
                request_data["tid"],
            "messages":
                [
                    {
                        "level": request_data["level"],
                        "key": request_data["key"],
                        "dsc": request_data["dsc"],
                    },
                ]
        }

    request_data["response_code"] = status.HTTP_200_OK
    request_data["status"] = BANCARD_STATUS_SUCCESS
    request_data["level"] = BANCARD_LEVEL_SUCCESS
    request_data["key"] = BANCARD_CODE_TRANSACTION_REVERSED
    request_data["dsc"] = ["Transacción reversada satisfactoriamente"]
    query = payment_requests.insert().values(request_data)
    await db.execute(query)

    response.status_code = request_data["response_code"]

    return {
        "status":
            request_data["status"],
        "tid":
            request_data["tid"],
        "messages":
            [
                {
                    "level": request_data["level"],
                    "key": request_data["key"],
                    "dsc": request_data["dsc"]
                }
            ],
    }
