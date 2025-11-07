from typing import ClassVar
from unittest import TestCase

import pytest

from crud.crud import AlreadyExistsError, storage
from schemas.movies_schema import CreateMovie, Movie, PartialUpdateMovie, UpdateMovie
from testing.test_api.conftest import create_movie_random_slug


class UpdateMovieTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie_random_slug()

    def tearDown(self) -> None:
        storage.delete(self.movie)

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


class MovieStorageGetMovieTestCase(TestCase):
    MOVIES_COUNTS = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie_random_slug() for _ in range(cls.MOVIES_COUNTS)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get_list()
        expected_slug = {su.slug for su in self.movies}
        slug_in_db = {su.slug for su in movies}
        expected_diff: set[Movie] = set()
        diff = expected_slug - slug_in_db
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can get slug {movie.slug!r}",
            ):
                db_movie = storage.get_by_slug(movie.slug)
                self.assertEqual(
                    movie,
                    db_movie,
                )


def test_create_of_raise_if_exists(movie: Movie) -> None:
    created_movie = CreateMovie(**movie.model_dump())
    with pytest.raises(
        expected_exception=AlreadyExistsError, match=movie.slug,
    ) as ex_info:
        storage.create_if_not_exist(film_in=created_movie)

    assert ex_info.value.args[0] == created_movie.slug
