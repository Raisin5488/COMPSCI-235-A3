import pytest
from movie_web_app.domain.user import User
from movie_web_app.domain.movie import Movie


def test_1():
    name = User("Banana", "abcd1234")
    assert name.username == "banana"
    assert name.password == "abcd1234"
    assert name.watched_movies == []
    assert name.watch_list.movie_list == []
    assert name.reviews == []
    assert name.time_spent_watching_movies_minutes == 0


def test_2():
    name = User("Banana", "abcd1234")
    movie = Movie("Moviename", 2020)
    movie.runtime_minutes = 100
    name.watch_movie(movie)
    name.add_review("123")
    name.watch_list.add_movie(movie)
    assert name.watched_movies == [movie]
    assert name.watch_list.movie_list == [movie]
    assert name.reviews == ["123"]
    assert name.time_spent_watching_movies_minutes == 100
