from fastapi import HTTPException
from starlette import status

from schemas.movies_schema import Movie
from crud.crud import storage


def prefetch_movie(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r}not found",
    )
