from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


@router.get("/")
def read_root(
    request: Request,
    name: str = "World",
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "massage": f"Hello {name}! Это сайт про фильмы",
        "docs": str(docs_url),
    }
