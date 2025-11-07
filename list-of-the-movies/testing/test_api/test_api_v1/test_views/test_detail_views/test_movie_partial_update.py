from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from starlette import status

from crud.crud import storage
from main import app
from schemas.movies_schema import Movie
from testing.test_api.conftest import create_movie_random_slug
from tools.const import MAX_DESCRIPTION

pytestmark = pytest.mark.apitest


class TestUpdatePartial:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        description = request.param
        movie = create_movie_random_slug(
            description=description,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie,new_description",
        [
            pytest.param(
                "some description",
                "",
                id="text-description-to-empty",
            ),
            pytest.param(
                "",
                "some description",
                id="empty-description-to-text",
            ),
            pytest.param(
                "a" * MAX_DESCRIPTION,
                "a",
                id="max-length-description-to-min",
            ),
            pytest.param(
                "a",
                "a" * MAX_DESCRIPTION,
                id="min-length-description-to-max",
            ),
        ],
        indirect=[
            "movie",
        ],
    )
    def test_update_movie_details_partial(
        self,
        movie: Movie,
        auth_client: TestClient,
        new_description: str,
    ) -> None:
        url = app.url_path_for("patch_movie", slug=movie.slug)
        response = auth_client.patch(url, json={"description": new_description})
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_from_db = storage.get_by_slug(movie.slug)
        assert movie_from_db
        assert movie_from_db.description == new_description
