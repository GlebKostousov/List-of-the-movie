from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.api_v1.service.auth.redis_auth import redis_token
from main import app


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app=app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = redis_token.generate_and_save_token()
    yield token
    redis_token.delete_token(token)


@pytest.fixture(scope="module")
def auth_client(auth_token: str) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app=app, headers=headers) as test_client:
        yield test_client
