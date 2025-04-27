from pydantic import BaseModel


class MovieBase(BaseModel):
    movie_id: int
    title: str
    year: int
    description: str
    duration: float


class Movie(MovieBase):
    """
    Класс для хранения данных о фильме
    """
