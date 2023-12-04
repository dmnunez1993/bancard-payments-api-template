from typing import Annotated, Dict, Any

from fastapi import HTTPException, status, Depends

from .api_key import verify_api_key


class PermissionRequired(object):
    def __init__(self, permission: str):
        self._permission = permission

    def __call__(
        self,
        api_key: Annotated[
            Dict[str, Any],
            Depends(verify_api_key),
        ],
    ):
        if self._permission not in api_key["permissions"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
