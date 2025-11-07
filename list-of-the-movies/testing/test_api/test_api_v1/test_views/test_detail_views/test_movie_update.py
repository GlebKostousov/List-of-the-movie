from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from starlette import status

from crud.crud import storage
from main import app
from schemas.movies_schema import Movie
from testing.test_api.conftest import create_movie_random_slug

pytestmark = pytest.mark.apitest


class TestUpdate:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        description, title = request.param
        movie = create_movie_random_slug(
            description=description,
            title=title,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_title, new_description",
        [
            pytest.param(
                ("some description", "example"), "new description", "new title", id="1",
            ),
            pytest.param(
                ("some description", "site"), "new description", "new title", id="2",
            ),
            pytest.param(
                ("some description", "empty"), "new description", "new title", id="3",
            ),
            pytest.param(
                ("some description", "some tit"), "new description", "new title", id="4",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        auth_client: TestClient,
        movie: Movie,
        new_title: str,
        new_description: str,
    ) -> None:
        url = app.url_path_for("update_movie", slug=movie.slug)
        data = movie.model_dump(mode="json")
        data["title"] = new_title
        data["description"] = new_description
        response = auth_client.put(url=url, json=data)
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_from_db = storage.get_by_slug(movie.slug)
        assert movie_from_db
        data_from_db = movie_from_db.model_dump(mode="json")
        assert data_from_db == data
