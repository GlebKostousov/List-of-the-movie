from unittest import TestCase

from schemas.movies_schema import CreateMovie, Movie, PartialUpdateMovie, UpdateMovie


class TestMovie(TestCase):
    movie = Movie(
        slug="some-sluggg",
        title="some titleeee",
        year=2000,
        description="some description",
        duration=200,
        notes="some notes",
    )

    def test_movie_can_be_created_from_create_movie(self) -> None:
        movie_in = CreateMovie(
            title="some title",
            year=1957,
            description="some description",
            duration=158,
            slug="some-slug",
        )
        movie: Movie = Movie.model_validate(movie_in.model_dump())
        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.year, movie.year)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.duration, movie.duration)
        self.assertEqual(movie_in.slug, movie.slug)

    def test_movie_can_be_created_from_update_movie(self) -> None:
        movie_in = UpdateMovie(
            title="some title",
            year=1957,
            description="some description",
            duration=158,
        )

        slug = self.movie.slug
        notes = self.movie.notes
        for field, value in movie_in:
            setattr(self.movie, field, value)

        self.assertEqual(movie_in.title, self.movie.title)
        self.assertEqual(movie_in.year, self.movie.year)
        self.assertEqual(movie_in.description, self.movie.description)
        self.assertEqual(movie_in.duration, self.movie.duration)
        self.assertEqual(slug, self.movie.slug)
        self.assertEqual(notes, self.movie.notes)

    def test_movie_can_be_created_from_partial_update_movie(self) -> None:
        movie_in_param = [
            ("some title", 1950, "some description", 180),
            (None, 1950, "some description", 180),
            ("some title", None, "some description", 180),
            ("some title", 1950, None, 180),
            ("some title", 1950, "some description", None),
        ]
        slug = self.movie.slug
        notes = self.movie.notes
        for title, year, description, duration in movie_in_param:
            with self.subTest(
                title=title,
                year=year,
                description=description,
                duration=duration,
            ):
                movie_in = PartialUpdateMovie(
                    title=title,
                    year=year,
                    description=description,
                    duration=duration,
                )
                for field, value in movie_in.model_dump(exclude_unset=True).items():
                    setattr(self.movie, field, value)

                self.assertEqual(movie_in.title, self.movie.title)
                self.assertEqual(movie_in.year, self.movie.year)
                self.assertEqual(movie_in.description, self.movie.description)
                self.assertEqual(movie_in.duration, self.movie.duration)
                self.assertEqual(slug, self.movie.slug)
                self.assertEqual(notes, self.movie.notes)
