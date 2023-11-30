from typing import List, Union

from api.common.router import create_api_router
from api.models.bancard import BancardResponse, InvoicesResponse

router = create_api_router()


@router.get(
    "/invoices", response_model=Union[BancardResponse, InvoicesResponse]
)
async def get_invoices(tid: int, prd_id: int, sub_id: List[int]):
    pass
