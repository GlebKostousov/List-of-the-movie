from fastapi import status
from starlette.testclient import TestClient
from main import app
from schemas.movies_schema import Movie
from testing.test_api.conftest import build_movie_create_random_slug


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    data: dict[str, str] = build_movie_create_random_slug().model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_data = {
        "title": response_data["title"],
        "year": response_data["year"],
        "description": response_data["description"],
        "duration": response_data["duration"],
        "slug": response_data["slug"],
    }
    assert received_data == data, response_data


def test_create_movie_already_exists(auth_client: TestClient, movie: Movie) -> None:
    url = app.url_path_for("create_movie")
    data: dict[str, str] = movie.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_detail = response.json()["detail"]
    expected_detail = f"Movie with slug={movie.slug!r} already exists"
    assert response_detail == expected_detail, response_detail
