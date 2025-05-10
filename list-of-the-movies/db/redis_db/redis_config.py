"""
Настройки для подключения Redis
"""

from typing import Final

REDIS_HOST: Final[str] = "localhost"
REDIS_PORT: Final[int] = 6379
REDIS_DB: Final[int] = 0
REDIS_TOKENS_DB: Final[int] = 1
REDIS_DECODE: Final[bool] = True
