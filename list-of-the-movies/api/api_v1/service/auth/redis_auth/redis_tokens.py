"""
Модуль для подключения БД Redis со статичными токенами авторизации
"""

from redis import Redis
import services.redis_config as rc

from api.api_v1.service.auth.abstract_tokens_wrapper import AbstractTokensHelper


class RedisTokensHelper(AbstractTokensHelper):
    """
    Класс для управления токенами с помощью Redis.
    Используем 3 метода:
    - token_exists
    - add_token
    - generate_and_save_token
    """

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        decode_responses: bool = False,
        set_tokens_name: str = "tokens",
    ):
        self.tokens_set = set_tokens_name
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    def token_exists(self, token_to_check: str) -> bool:
        return bool(
            self.redis.sismember(
                name=self.tokens_set,
                value=token_to_check,
            )
        )

    def add_token(self, token_to_add: str) -> None:
        self.redis.sadd(
            name=self.tokens_set,
            *token_to_add,
        )

    def get_all_tokens(self) -> list[str]:
        return list(self.redis.smembers(name=self.tokens_set))


redis_token = RedisTokensHelper(
    host=rc.REDIS_HOST,
    port=rc.REDIS_PORT,
    db=rc.REDIS_TOKENS_DB,
    decode_responses=rc.REDIS_DECODE,
    set_tokens_name=rc.REDIS_TOKENS_SET_NAME,
)
