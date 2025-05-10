"""
Модуль для подключения БД Redis со статичными токенами авторизации
"""

from redis import Redis
import db.redis_db.redis_config as rc


redis_token = Redis(
    host=rc.REDIS_HOST,
    port=rc.REDIS_PORT,
    db=rc.REDIS_TOKENS_DB,
    decode_responses=rc.REDIS_DECODE,
)
