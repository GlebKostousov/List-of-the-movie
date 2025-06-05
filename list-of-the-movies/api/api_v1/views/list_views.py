from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from crud.crud import AlreadyExistsError, storage
from dependencies.auth_required import auth_required
from schemas.movies_schema import (
    CreateMovie,
    Movie,
    MovieRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
    dependencies=[
        Depends(auth_required),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication error",  # Текстовое описание ответа
            "content": {  # Описание формата тела ответа
                "application/json": {  # JSON-ответ
                    "example": {  # пример тела ответа
                        # техническая информация для разработчиков!
                        "detail": "APIkey invalid. Only for unsafe methods",
                    },
                },
            },
        },
    },
)


@router.get("/", response_model=list[MovieRead])
def read_list_of_films() -> list[Movie]:
    return storage.get_list()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Movie already exist",  # Текстовое описание ответа
            "content": {  # Описание формата тела ответа
                "application/json": {  # JSON-ответ
                    "example": {  # пример тела ответа
                        # техническая информация для разработчиков!
                        "detail": "Movie with slug='name' already exists",
                    },
                },
            },
        },
    },
)
def create_movie(
    movie_create: CreateMovie,
) -> Movie:
    try:
        return storage.create_if_not_exist(movie_create)
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={movie_create.slug!r} already exists",
        ) from None
