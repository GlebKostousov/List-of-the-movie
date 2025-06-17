import random
import string
from os import getenv
from unittest import TestCase

from crud.crud import storage
from schemas.movies_schema import CreateMovie, Movie, PartialUpdateMovie, UpdateMovie

if getenv("TESTING") != "1":
    error_testing_msg = "Environment is not ready for testing"
    raise OSError(error_testing_msg)


class UpdateMovieTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    @classmethod
    def create_movie(cls) -> Movie:
        created_movie = CreateMovie(
            title="title",
            year=1999,
            description="description",
            duration=150,
            slug="".join(random.choices(string.ascii_letters, k=6)),
        )
        return storage.create(created_movie)

    def test_update_movie(self) -> None:
        source_description = self.movie.description
        movie_in = UpdateMovie(**self.movie.model_dump())
        movie_in.description *= 2
        updated_movie = storage.update(
            self.movie,
            movie_in,
        )

        self.assertNotEqual(source_description, updated_movie.description)
        self.assertEqual(updated_movie, self.movie)

    def test_partial_update_movie(self) -> None:
        source_description = self.movie.description
        movie_in = PartialUpdateMovie(**self.movie.model_dump())
        movie_in.description = "description_2"
        partial_updated_movie = storage.partial_update(
            self.movie,
            movie_in,
        )
        self.assertNotEqual(source_description, partial_updated_movie.description)
        self.assertEqual(partial_updated_movie, self.movie)
