from typing import Generic, TypeVar, Optional, List

from pydantic import Field

from api.models.base import BaseModel

M = TypeVar("M", bound=BaseModel)


class Message(BaseModel):
    level: str
    key: str
    dsc: List[str]


class CommerceData(BaseModel):
    cmr_id: int
    cmr_bra: int
    srv_data: List[str]
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
    barcode: str


class PaymentSuccessfulResponse(BancardResponse):
    tkt: int
    aut_cod: int
    prnt_msg: List[str]


class ReversalRequest(BaseModel):
    tid: int
