from fastapi import (
    HTTPException,
    APIRouter,
)

from schemas.movies_schema import Movie
from services.const import MOVIES_LIST

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


def get_film_by_id(movie_id: int) -> Movie | None:
    result: Movie | None = next(
        (movie for movie in MOVIES_LIST if movie.movie_id == movie_id), None
    )
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Не найден фильм с id={movie_id}")


@router.get("/{movie_id}")
def read_movie(movie_id: int):
    return get_film_by_id(movie_id)


@router.get("/list")
def read_list_of_films():
    return MOVIES_LIST
