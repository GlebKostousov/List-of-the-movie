import pytest
from fastapi.testclient import TestClient
from starlette import status

from main import app


@pytest.mark.apitest
@pytest.mark.xfail(
    reason="Not ready yet",
    raises=NotImplementedError,
    strict=True,
)
def test_transfer_movie(auth_client: TestClient) -> None:
    url = app.url_path_for(
        "transfer_movie",
        slug="test",
    )
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK, response.text
