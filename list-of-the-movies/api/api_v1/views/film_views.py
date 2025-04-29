from typing import List, Annotated

from fastapi import (
    HTTPException,
    APIRouter,
    status,
)
from fastapi.params import Depends

from schemas.movies_schema import Movie, CreateMovie
from crud.crud import storage
from dependencies.prefetch_movie import prefetch_movie

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


@router.get("/{slug}", response_model=Movie)
def read_movie(movie: Annotated[Movie, Depends(prefetch_movie)]) -> Movie | None:
    return movie


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "FILM 'slug' not found",
                    },
                },
            },
        },
    },
)
def delete_movie(movie: Annotated[Movie, Depends(prefetch_movie)]) -> None:
    storage.delete(film_in=movie)


@router.get("/", response_model=List[Movie])
def read_list_of_films() -> List[Movie]:
    return storage.get_list()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie_create: CreateMovie) -> Movie:
    return storage.create(film_in=movie_create)
