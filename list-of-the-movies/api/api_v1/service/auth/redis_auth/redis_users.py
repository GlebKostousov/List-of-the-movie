"""
Модуль для подключения БД Redis с username и password авторизации
"""

from typing import cast

from redis import Redis

import tools.redis_config as rc
from api.api_v1.service.auth.abstract_users_wrapper import AbstractUsersHelper


class RedisUsersHelper(AbstractUsersHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        *,
        decode_responses: bool = False,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    def get_password_from_db(self, username: str) -> str | None:
        if self.redis.exists(username):
            return cast(str | None, self.redis.get(username))

        return None

    def add_username_and_password_to_db(
        self,
        username_to_add: str,
        password_to_add: str,
    ) -> None:
        self.redis.set(name=username_to_add, value=password_to_add)


redis_users = RedisUsersHelper(
    host=rc.REDIS_HOST,
    port=rc.REDIS_PORT,
    db=rc.REDIS_USERS_DB,
    decode_responses=rc.REDIS_DECODE,
)
