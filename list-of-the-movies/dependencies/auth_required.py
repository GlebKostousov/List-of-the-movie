from fastapi import (
    Request,
    status,
    HTTPException,
)
from typing import Annotated

from fastapi.params import Depends

from services.const import (
    UNSAFE_METHODS,
    FAKE_USERNAME_DB,
    REDIS_TOKEN_SET_NAME,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)
from db.redis_db.redis_tokens import redis_token
import logging

log = logging.getLogger(__name__)

static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="Your **API token from developer** portal. [Readme more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="User basic auth",
    description="Basic username + password auth",
    auto_error=False,
)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    log.info("Received %r API token", api_token)
    if redis_token.sismember(
        name=REDIS_TOKEN_SET_NAME,
        value=api_token.credentials,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You APIkey invalid",
    )


def validate_basic_user(
    credentials: HTTPBasicCredentials,
):
    log.info("User auth credentials %s", credentials)
    if (
        credentials.username in FAKE_USERNAME_DB
        and FAKE_USERNAME_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def auth_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if api_token:
        return validate_api_token(api_token=api_token)

    if credentials:
        return validate_basic_user(credentials=credentials)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect api token or credentials",
    )
