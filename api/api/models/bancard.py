from typing import List

from pydantic import Field

from api.models.base import BaseModel

BANCARD_STATUS_ERROR = "error"
BANCARD_STATUS_SUCCESS = "success"
BANCARD_LEVEL_ERROR = "error"
BANCARD_LEVEL_SUCCESS = "success"
BANCARD_LEVEL_INFO = "info"
BANCARD_CODE_SUBSCRIBER_NOT_FOUND = "SubscriberNotFound"
BANCARD_CODE_SUBSCRIBER_WITHOUT_DEBT = "SubscriberWithoutDebt"
BANCARD_CODE_INVALID_PARAMETERS = "InvalidParameters"
BANCARD_CODE_MISSING_PARAMETER = "MissingParameter"
BANCARD_CODE_OVERDUE_INVOICE = "OverdueInvoice"
BANCARD_CODE_UNKNOWN_ERROR = "UnknownError"
BANCARD_CODE_HOST_TRANSACTION_ERROR = "HostTransactionError"
BANCARD_CODE_PAYMENT_NOT_AUTHORIZED = "PaymentNotAuthorized"
BANCARD_CODE_PAYMENT_PROCESSED = "PaymentProcessed"
BANCARD_CODE_QUERY_PROCESSED = "QueryProcessed"
BANCARD_CODE_TRANSACTION_NOT_REVERSED = "TransactionNotReversed"
BANCARD_CODE_TRANSACTION_REVERSED = "TransactionReversed"


class Message(BaseModel):
    level: str
    key: str
    dsc: List[str]


class CommerceData(BaseModel):
    cmr_id: int
    cmr_bra: int
    srv_dta: List[str]
    payment_method: str


class BancardResponse(BaseModel):
    status: str
    tid: int
    messages: List[Message]


class Due(BaseModel):
    amt: float
    date: str


class Invoice(BaseModel):
    due: str
    amt: float
    min_amt: float
    inv_id: List[str]
    curr: str
    addl: List[str]
    next_dues: List[Due]
    cm_amt: float | None = Field(default=None)
    cm_curr: str | None = Field(default=None)
    dsc: str


class InvoicesResponse(BancardResponse):
    invoices: List[Invoice] | None = Field(default=None)


class PaymentRequest(BaseModel):
    tid: int
    prd_id: int
    sub_id: List[str]
    inv_id: List[str]
    amt: float
    curr: str
    trn_dat: str
    trn_hou: int
    cm_amt: float | None = Field(default=None)
    cm_curr: str | None = Field(default=None)
    addl: CommerceData
    type: str
    barcode: str | None = Field(default=None)


class PaymentSuccessfulResponse(BancardResponse):
    tkt: int | None = Field(default=None)
    aut_cod: int | None = Field(default=None)
    prnt_msg: List[str] | None = Field(default=None)


class ReversalRequest(BaseModel):
    tid: int
