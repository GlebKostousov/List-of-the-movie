from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from starlette import status

from crud.crud import storage
from main import app
from schemas.movies_schema import Movie
from testing.test_api.conftest import create_movie_random_slug, build_movie_create


def create_short_url(slug: str) -> Movie:
    created_movie = build_movie_create(
        slug=slug,
        description="description",
        year=1999,
        title="title",
        duration=150.0,
    )
    return storage.create(created_movie)


@pytest.fixture(
    params=[
        pytest.param("some_slug", id="some-slug"),
        pytest.param("123", id="short-slug"),
        pytest.param("s" * 30, id="long-slug"),
        pytest.param("some_slug", id="some_slug"),
    ]
)
def movie(request: SubRequest) -> Generator[Movie]:
    movie = create_short_url(request.param)
    yield movie
    storage.delete(movie)


def test_delete_movie(auth_client: TestClient, movie: Movie) -> None:
    url = app.url_path_for("delete_movie", slug=movie.slug)
    assert storage.exists(movie.slug), f"{movie.slug} does not exist before deletion"
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug), f"{movie.slug} exists after deletion"
