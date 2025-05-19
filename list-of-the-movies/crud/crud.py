from typing import Dict, List

from pydantic import BaseModel, ValidationError
from redis import Redis

from schemas.movies_schema import Movie, CreateMovie, UpdateMovie, PartialUpdateMovie
from services.const import DB_PATH
from services.logger import log
import services.redis_config as rc

redis_films = Redis(
    host=rc.REDIS_HOST,
    port=rc.REDIS_PORT,
    db=rc.REDIS_FILMS_DB,
    decode_responses=rc.REDIS_DECODE,
)


class MovieStorage(BaseModel):
    slug_to_film: Dict[str, Movie] = {}

    def init_storage_from_state(self) -> None:
        try:
            data = MovieStorage.load_state()
        except ValidationError:
            self.save_state()
            log.warning("Не получилось загрузить файл ДБ. Создаем новый")
            return

        self.slug_to_film.update(data.slug_to_film)
        log.warning("Данные с диск загружены")

    @classmethod
    def load_state(cls) -> "MovieStorage":
        if not DB_PATH.exists():
            log.info(f"DB_PATH не существует. Создал новый!")
            return MovieStorage()
        return cls.model_validate_json(DB_PATH.read_text())

    def save_state(self) -> None:
        DB_PATH.write_text(self.model_dump_json(indent=2))
        log.warning("Сохранил данные в JSON")

    def get_list(self) -> List[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in redis_films.hvals(name=rc.REDIS_FILMS_SET_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if film_json := redis_films.hget(
            name=rc.REDIS_FILMS_SET_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(film_json)

    def create(self, film_in: CreateMovie) -> Movie:
        film = Movie(**film_in.model_dump())
        redis_films.hset(
            name=rc.REDIS_FILMS_SET_NAME,
            key=film.slug,
            value=film.model_dump_json(),
        )
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)

    def delete(self, film_in: Movie) -> None:
        return self.delete_by_slug(slug=film_in.slug)

    def update(self, film: Movie, film_in: UpdateMovie) -> Movie:
        for field, value in film_in:
            setattr(film, field, value)
        return film

    def partial_update(self, film: Movie, film_in: PartialUpdateMovie) -> Movie:
        for field, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field, value)
        return film


storage = MovieStorage()
