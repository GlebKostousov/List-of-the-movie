from fastapi import (
    Request,
    status,
    HTTPException,
)
from typing import Annotated

from fastapi.params import Depends

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)
from api.api_v1.service.auth.redis_auth import (
    redis_users,
    redis_token,
)
import logging

from services.const import UNSAFE_METHODS

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
    if redis_token.token_exists(
        token_to_check=api_token.credentials,
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
    if credentials and redis_users.verified_password_is_correct(
        username_in=credentials.username,
        password_in=credentials.password,
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
