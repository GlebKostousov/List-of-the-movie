from typing import Final

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
)
from schemas.movies_schema import Movie

MOVIES_LIST: Final[list[Movie]] = [
    Movie(
        movie_id=1,
        title="Землетрясение",
        year=2010,
        description="28 июля 1976 года в Таншане провинции Хэбэй произошло землетрясение, которое длилось меньше чем полминуты, но унесло несколько сотен тысяч жизней. Эти секунды поставили мать перед ужасным выбором — спасти сына или дочь, что обернулось грузом вины на десятилетия.",
        duration=139,
    ),
    Movie(
        movie_id=2,
        title="Пол: Секретный материальчик",
        year=2011,
        description="Два британских гика отправляются на одно из самых значимых фанатских событий в области фантастики — конвент ComicCon в Америке. По пути, неподалёку от известной Зоны 51, они встречают сбежавшего инопланетянина по имени Пол, который просит помочь ему добраться домой.",
        duration=139,
    ),
    Movie(
        movie_id=3,
        title="Ночь на Земле",
        year=1991,
        description="Пять таксистских историй, случившихся за одну ночь в пяти городах мира: Лос-Анджелесе, Нью-Йорке, Париже, Риме и Хельсинки.",
        duration=129,
    ),
]

app = FastAPI(
    title="List of the Movies",
)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "massage": f"Hello {name}! Это сайт про фильмы",
        "docs": str(docs_url),
    }


def get_film_by_id(movie_id: int) -> Movie | None:
    result: Movie | None = next(
        (movie for movie in MOVIES_LIST if movie.movie_id == movie_id), None
    )
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Не найден фильм с id={movie_id}")


@app.get("/movies")
def read_list_of_films():
    return MOVIES_LIST


@app.get("/movies/{movie_id}")
def read_movie(movie_id: int):
    return get_film_by_id(movie_id)
