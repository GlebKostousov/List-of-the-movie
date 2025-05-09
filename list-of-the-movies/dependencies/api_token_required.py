from fastapi import (
    Request,
    status,
    Query,
    HTTPException,
)
from typing import Annotated
from services.const import (
    UNSAFE_METHODS,
    API_TOKENS,
)


def api_token_required(
    request: Request,
    api_token: Annotated[str, Query()] = "",
):
    if request.method not in UNSAFE_METHODS:
        return

    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You APIkey invalid",
        )
