from typing import Annotated, Dict, Any

from fastapi import Header, HTTPException, status

from auth.api_key import validate_key


async def verify_api_key(x_api_key: Annotated[str, Header()]) -> Dict[str, Any]:
    api_key_data = await validate_key(x_api_key)

    if api_key_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return api_key_data
