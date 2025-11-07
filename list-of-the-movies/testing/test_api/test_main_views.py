import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)


@pytest.mark.apitest
@pytest.mark.parametrize(
    "name",
    [
        "john",
        "",
        "!@#$",
        "Jpgm Smith",
    ],
)
def test_root_view(name: str) -> None:
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == 200
    response_data = response.json()
    expected_data = f"Hello {name}! Это сайт про фильмы"
    assert expected_data == response_data["massage"], response_data
