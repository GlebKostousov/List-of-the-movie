from typing import List

from fastapi import (
    APIRouter,
    status,
    Depends,
)

from dependencies.api_token_required import api_token_required
from schemas.movies_schema import (
    Movie,
    CreateMovie,
    MovieRead,
)
from crud.crud import storage
from dependencies.storage_save_state_background import storage_save_state_background

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
    dependencies=[Depends(storage_save_state_background), Depends(api_token_required)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication credentials were not provided.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You APIkey invalid",
                    },
                },
            },
        },
    },
)


@router.get("/", response_model=List[MovieRead])
def read_list_of_films() -> List[Movie]:
    return storage.get_list()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_create: CreateMovie,
) -> Movie:
    return storage.create(film_in=movie_create)
