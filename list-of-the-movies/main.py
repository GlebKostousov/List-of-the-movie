from fastapi import (
    FastAPI,
    Request,
)
from api import router as api_router
from api.app_lifespan import lifespan

app = FastAPI(title="Сайт про фильмы", lifespan=lifespan)
app.include_router(api_router)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "massage": f"Hello {name}! Это сайт про фильмы",
        "docs": str(docs_url),
    }
