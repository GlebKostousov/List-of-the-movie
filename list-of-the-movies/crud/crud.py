from typing import List

from pydantic import BaseModel
from redis import Redis

from schemas.movies_schema import Movie, CreateMovie, UpdateMovie, PartialUpdateMovie
import services.redis_config as rc

redis_films = Redis(
    host=rc.REDIS_HOST,
    port=rc.REDIS_PORT,
    db=rc.REDIS_FILMS_DB,
    decode_responses=rc.REDIS_DECODE,
)


class MovieStorage(BaseModel):

    @classmethod
    def delete_by_slug(cls, slug: str) -> None:
        redis_films.hdel(
            rc.REDIS_FILMS_SET_NAME,
            slug,
        )

    @classmethod
    def save_movie(cls, film: Movie) -> None:
        redis_films.hset(
            name=rc.REDIS_FILMS_SET_NAME,
            key=film.slug,
            value=film.model_dump_json(),
        )

    @classmethod
    def get_list(cls) -> List[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in redis_films.hvals(name=rc.REDIS_FILMS_SET_NAME)
        ]

    @classmethod
    def get_by_slug(cls, slug: str) -> Movie | None:
        if film_json := redis_films.hget(
            name=rc.REDIS_FILMS_SET_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(film_json)

    def create(self, film_in: CreateMovie) -> Movie:
        film = Movie(**film_in.model_dump())
        self.save_movie(film)
        return film

    def delete(self, film_in: Movie) -> None:
        return self.delete_by_slug(slug=film_in.slug)

    def update(self, film: Movie, film_in: UpdateMovie) -> Movie:
        for field, value in film_in:
            setattr(film, field, value)

        self.save_movie(film)
        return film

    def partial_update(self, film: Movie, film_in: PartialUpdateMovie) -> Movie:
        for field, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field, value)

        self.save_movie(film)
        return film


storage = MovieStorage()
