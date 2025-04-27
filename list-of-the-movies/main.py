from fastapi import (
    FastAPI,
    Request,
    HTTPException,
)
from schemas.movies_schema import Movie
from services.const import MOVIES_LIST

app = FastAPI(
    title="List of the Movies",
)


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


def get_film_by_id(movie_id: int) -> Movie | None:
    result: Movie | None = next(
        (movie for movie in MOVIES_LIST if movie.movie_id == movie_id), None
    )
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Не найден фильм с id={movie_id}")


@app.get("/movies")
def read_list_of_films():
    return MOVIES_LIST


@app.get("/movies/{movie_id}")
def read_movie(movie_id: int):
    return get_film_by_id(movie_id)
