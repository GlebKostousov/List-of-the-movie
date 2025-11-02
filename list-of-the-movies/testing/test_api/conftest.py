import random
import string
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.api_v1.service.auth.redis_auth import redis_token
from crud.crud import storage
from main import app
from schemas.movies_schema import Movie, CreateMovie


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


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = crate_and_save_movie()
    yield movie
    storage.delete(movie)


def create_movie() -> CreateMovie:
    return CreateMovie(
        title="title",
        year=1999,
        description="description",
        duration=150,
        slug="".join(random.choices(string.ascii_letters, k=6)),
    )


def crate_and_save_movie() -> Movie:
    created_movie = create_movie()
    return storage.create(created_movie)
