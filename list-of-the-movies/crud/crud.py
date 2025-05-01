from typing import Dict, List

from pydantic import BaseModel

from schemas.movies_schema import Movie, CreateMovie, UpdateMovie


class ShortUrlsStorage(BaseModel):
    slug_to_film: Dict[str, Movie] = {}  # ключ - slug

    def get_list(self) -> List[Movie]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Movie:
        return self.slug_to_film.get(slug)

    def create(self, film_in: CreateMovie) -> Movie:
        film = Movie(**film_in.model_dump())
        self.slug_to_film[film.slug] = film
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)

    def delete(self, film_in: Movie) -> None:
        return self.delete_by_slug(slug=film_in.slug)

    def update(self, film: Movie, film_in: UpdateMovie) -> Movie:
        for field, value in film_in:
            setattr(film, field, value)
        return film


storage = ShortUrlsStorage()

storage.create(
    film_in=CreateMovie(
        title="Землетрясение",
        slug="Землетрясение",
        year=2010,
        description="28 июля 1976 года в Таншане провинции Хэбэй произошло землетрясение, которое длилось меньше чем полминуты, но унесло несколько сотен тысяч жизней. Эти секунды поставили мать перед ужасным выбором — спасти сына или дочь, что обернулось грузом вины на десятилетия.",
        duration=139,
    )
)

storage.create(
    film_in=CreateMovie(
        title="Пол: Секретный материальчик",
        slug="Пол",
        year=2011,
        description="Два британских гика отправляются на одно из самых значимых фанатских событий в области фантастики — конвент ComicCon в Америке. По пути, неподалёку от известной Зоны 51, они встречают сбежавшего инопланетянина по имени Пол, который просит помочь ему добраться домой.",
        duration=139,
    )
)
storage.create(
    film_in=CreateMovie(
        title="Ночь на Земле",
        slug="ННЗ",
        year=1991,
        description="Пять таксистских историй, случившихся за одну ночь в пяти городах мира: Лос-Анджелесе, Нью-Йорке, Париже, Риме и Хельсинки.",
        duration=129,
    )
)
