from pydantic import BaseModel
from typing import Annotated
from annotated_types import Ge, Len, MaxLen

"--------- Аннотации --------------------------------"
Slug = Annotated[str, Len(3, 30)]
Title = Annotated[str, Len(min_length=3, max_length=50)]
Year = Annotated[int, Ge(1950)]
Duration = Annotated[float, Ge(5)]
Description = Annotated[str, MaxLen(200)]


class MovieBase(BaseModel):
    """
    Базовая модель только для наследования
    """

    title: Title
    year: Year
    description: str = ""
    duration: Duration


class Movie(MovieBase):
    """
    Класс для хранения и вывода данных о фильме
    """

    slug: Slug
    notes: str = ""


class MovieRead(MovieBase):
    """
    Модель для ответа на запрос
    """

    slug: str


class CreateMovie(MovieBase):
    """
    Модель для добавления нового фильма
    """

    slug: Slug


class UpdateMovie(MovieBase):
    """
    Модель для полного обновления информации о фильме
    """

    description: Description = ""


class PartialUpdateMovie(BaseModel):
    """
    Модель для частичного обновления данных Movie
    """

    title: Title | None = None
    year: Year | None = None
    description: Description | None = None
    duration: Duration | None = None
