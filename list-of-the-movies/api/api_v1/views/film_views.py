from typing import List, Annotated

from fastapi import (
    HTTPException,
    APIRouter,
    status,
    Form,
)
from pydantic.fields import Field

from schemas.movies_schema import Movie, CreateMovie
from services.const import MOVIES_LIST

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


def get_film_by_id(slug: str) -> Movie | None:
    result: Movie | None = next(
        (movie for movie in MOVIES_LIST if movie.slug.lower() == slug.lower()), None
    )
    if result:
        return result
    raise HTTPException(
        status_code=404, detail=f"Не найден фильм с сокращением  {slug}"
    )


@router.get("/{slug}", response_model=Movie)
def read_movie(slug: str) -> Movie | None:
    return get_film_by_id(slug)


@router.get("/", response_model=List[Movie])
def read_list_of_films() -> List[Movie]:
    return MOVIES_LIST


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie_create: CreateMovie) -> Movie:
    return Movie(**movie_create.model_dump())
