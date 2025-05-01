from pydantic import BaseModel
from typing import Annotated
from annotated_types import Ge, Len, MaxLen


class MovieBase(BaseModel):
    # noinspection PyTypeHints
    title: Annotated[str, Len(min_length=3, max_length=50)]
    year: Annotated[int, Ge(1950)]
    description: str = ""
    duration: Annotated[float, Ge(5.0)]


class Movie(MovieBase):
    """
    Класс для хранения данных о фильме
    """

    # noinspection PyTypeHints
    slug: Annotated[str, Len(3, 30)]


class CreateMovie(MovieBase):
    """
    Модель для добавления нового фильма
    """

    # noinspection PyTypeHints
    slug: Annotated[str, Len(3, 30)]


class UpdateMovie(MovieBase):
    """
    Модель для обновления информации о фильме
    """

    description: Annotated[str, MaxLen(200)] = ""
