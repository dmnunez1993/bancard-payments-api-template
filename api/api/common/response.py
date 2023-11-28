from typing import Generic, TypeVar, Optional, List

from api.models.base import BaseModel

M = TypeVar("M", bound=BaseModel)


class Response(BaseModel):
    status: str


class ListData(BaseModel, Generic[M]):
    count: int
    items: List[M]


class ListResponse(Response, Generic[M]):
    data: ListData[M]


class ItemResponse(Response, Generic[M]):
    data: Optional[M] = None


class ErrorResponse(Response):
    detail: str


class SuccessResponse(Response):
    pass
