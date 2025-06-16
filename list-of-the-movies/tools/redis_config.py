"""
Настройки для подключения Redis
"""

from os import getenv
from typing import Final

REDIS_HOST: Final[str] = "localhost"
REDIS_PORT: Final[int] = int(getenv("REDIS_PORT", "0")) or 6379
REDIS_DECODE: Final[bool] = True

REDIS_TOKENS_DB: Final[int] = 1
REDIS_TOKENS_SET_NAME: Final[str] = "tokens"

REDIS_USERS_DB: Final[int] = 2

REDIS_FILMS_DB: Final[int] = 3
REDIS_FILMS_SET_NAME: Final[str] = "films"
