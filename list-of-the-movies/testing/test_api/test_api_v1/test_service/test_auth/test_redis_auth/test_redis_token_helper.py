from os import getenv
from unittest import TestCase

from api.api_v1.service.auth.redis_auth import redis_token

if getenv("TESTING") != "1":
    error_testing_msg = "Environment is not ready for testing"
    raise OSError(error_testing_msg)


class TestRedisTokenHelper(TestCase):
    def test_generate_and_save_token(self) -> None:
        new_token = redis_token.generate_and_save_token()
        self.assertTrue(
            redis_token.token_exists(token_to_check=new_token),
        )
