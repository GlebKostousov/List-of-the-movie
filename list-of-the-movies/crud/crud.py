import json
from typing import Dict, List

from pydantic import BaseModel

from schemas.movies_schema import Movie, CreateMovie, UpdateMovie, PartialUpdateMovie
from services.tools import get_project_root
from pathlib import Path


def open_db_json(path: Path) -> Dict[str, Movie]:
    result: Dict[str, Movie] = {}
    if not path.exists():
        return result
    try:
        with open(path, "r", encoding="utf-8") as f:
            movies = json.load(f)

        for movie in movies:
            try:
                mov: Movie = Movie.model_validate(movie)
                if mov.slug:
                    result[mov.slug] = mov

            except ValueError as e:
                print(e)

    except (UnicodeDecodeError, json.JSONDecodeError):
        return result

    return result


class ShortUrlsStorage(BaseModel):
    db_path: Path = Path(get_project_root() / "db" / "movies.json")
    slug_to_film: Dict[str, Movie] = open_db_json(path=db_path)  # ключ - slug

    def lst_json_str(self) -> List[str]:
        result: List[str] = []
        for movie in self.slug_to_film.values():
            result.append(movie.model_dump())

        return result

    def save_to_db(self):
        data = self.lst_json_str()
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_list(self) -> List[Movie]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Movie:
        return self.slug_to_film.get(slug)

    def create(self, film_in: CreateMovie) -> Movie:
        film = Movie(**film_in.model_dump())
        self.slug_to_film[film.slug] = film
        self.save_to_db()
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)
        self.save_to_db()

    def delete(self, film_in: Movie) -> None:
        return self.delete_by_slug(slug=film_in.slug)

    def update(self, film: Movie, film_in: UpdateMovie) -> Movie:
        for field, value in film_in:
            setattr(film, field, value)
        self.save_to_db()
        return film

    def partial_update(self, film: Movie, film_in: PartialUpdateMovie) -> Movie:
        for field, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field, value)
        self.save_to_db()
        return film


storage = ShortUrlsStorage()
