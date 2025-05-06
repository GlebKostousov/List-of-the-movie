from typing import Annotated

from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends
from starlette import status

from crud.crud import storage
from dependencies.prefetch_movie import prefetch_movie
from schemas.movies_schema import Movie, UpdateMovie, PartialUpdateMovie, MovieRead

router = APIRouter(
    prefix="/{slug}",
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

Movie_By_Slug = Annotated[Movie, Depends(prefetch_movie)]


@router.get(
    "/",
    response_model=MovieRead,
)
def read_movie(
    movie: Movie_By_Slug,
) -> Movie | None:
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: Movie_By_Slug,
) -> None:
    storage.delete(film_in=movie)


@router.put(
    path="/",
    response_model=MovieRead,
)
def update_movie(
    movie: Movie_By_Slug,
    movie_in: UpdateMovie,
) -> Movie | None:
    return storage.update(film=movie, film_in=movie_in)


@router.patch(path="/", response_model=MovieRead)
def patch_movie(
    movie: Movie_By_Slug,
    movie_in: PartialUpdateMovie,
) -> Movie:
    return storage.partial_update(film=movie, film_in=movie_in)
