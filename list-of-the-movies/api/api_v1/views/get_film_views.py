from typing import List, Annotated

from fastapi import (
    HTTPException,
    APIRouter,
    status,
    Form,
)
from pydantic.fields import Field

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


@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int):
    return get_film_by_id(movie_id)


@router.get("/", response_model=List[Movie])
def read_list_of_films():
    return MOVIES_LIST


@router.post(
    path="/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    title: Annotated[str, Field(min_length=3, max_length=20), Form()],
    year: Annotated[int, Field(ge=1950), Form()],
    description: Annotated[str, Field(min_length=10), Form()],
    duration: Annotated[float, Field(ge=5.0), Form()],
):
    MOVIES_LIST.append(
        Movie(
            movie_id=len(MOVIES_LIST) + 1,
            title=title,
            year=year,
            description=description,
            duration=duration,
        )
    )
    return MOVIES_LIST[-1]
