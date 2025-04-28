from pydantic import BaseModel
from typing import Annotated
from annotated_types import Ge, Len


class MovieBase(BaseModel):
    # noinspection PyTypeHints
    title: Annotated[str, Len(min_length=3, max_length=50)]
    year: Annotated[int, Ge(1950)]
    # noinspection PyTypeHints
    description: Annotated[str, Len(min_length=10)]
    duration: Annotated[float, Ge(5.0)]
    # noinspection PyTypeHints
    slug: Annotated[str, Len(3, 30)]


class Movie(MovieBase):
    """
    Класс для хранения данных о фильме
    """


class CreateMovie(MovieBase):
    """
    Модель для добавления нового фильма
    """
