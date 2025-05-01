from typing import List

from fastapi import (
    APIRouter,
    status,
)

from schemas.movies_schema import Movie, CreateMovie
from crud.crud import storage

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


@router.get("/", response_model=List[Movie])
def read_list_of_films() -> List[Movie]:
    return storage.get_list()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie_create: CreateMovie) -> Movie:
    return storage.create(film_in=movie_create)
