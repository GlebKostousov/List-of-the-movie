from fastapi import status
import pytest
from starlette.testclient import TestClient
from main import app
from testing.test_crud.test_crud import create_movie


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    data: dict[str, str] = create_movie().model_dump(mode="json")
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
