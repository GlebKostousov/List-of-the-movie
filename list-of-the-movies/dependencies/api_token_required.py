from fastapi import (
    Request,
    status,
    HTTPException,
)
from typing import Annotated

from fastapi.params import Depends

from services.const import (
    UNSAFE_METHODS,
    API_TOKENS,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
import logging

log = logging.getLogger(__name__)

static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="Your **API token from developer** portal. [Readme more](#)",
    auto_error=False,
)


def api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("Received %r API token", api_token)
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empty API token",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You APIkey invalid",
        )
