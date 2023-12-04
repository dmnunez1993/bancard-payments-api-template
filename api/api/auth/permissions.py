from typing import Annotated, Dict, Any

from fastapi import Depends, Header, HTTPException, status

from auth.api_key import validate_key


async def verify_api_key(x_api_key: Annotated[str, Header()]) -> Dict[str, Any]:
    api_key_data = await validate_key(x_api_key)

    if api_key_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return api_key_data


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
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
