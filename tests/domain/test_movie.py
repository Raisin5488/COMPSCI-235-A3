import pytest
from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director
from movie_web_app.domain.movie import Movie


@pytest.fixture
def movie():
    return Movie("Moana", 2016)


def test_given(movie):
    movie = Movie("Moana", 2016)
    assert movie == Movie("Moana", 2016)

    director = Director("Ron Clements")
    movie.director = director
    assert movie.director == Director("Ron Clements")

    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie.add_actor(actor)
    assert movie.actors == actors

    movie.runtime_minutes = 107
    assert movie.runtime_minutes == 107


def test_rating(movie):
    movie = Movie("Moana", 2016)
    movie.rating = 9.5
    assert movie.rating == 9.5


def test_rating_out_bounds_lower(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.rating = -1


def test_rating_out_bounds_upper(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.rating = 10.5


def test_rating_type(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.rating = "banana"


def test_votes(movie):
    movie = Movie("Moana", 2016)
    movie.votes = 12345
    assert movie.votes == 12345


def test_votes_out_of_bounds(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.votes = -1


def test_votes_type(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.votes = 1234.5


def test_revenue_millions(movie):
    movie = Movie("Moana", 2016)
    movie.revenue_millions = 123.45
    assert movie.revenue_millions == 123.45


def test_revenue_millions_out_of_bounds(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.revenue_millions = -1


def test_revenue_millions_type(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.revenue_millions = "banana"


def test_metascore(movie):
    movie = Movie("Moana", 2016)
    movie.metascore = 93
    assert movie.metascore == 93


def test_metascore_out_of_bounds_lower(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.metascore = -1


def test_metascore_out_of_bounds_upper(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.metascore = 101


def test_metascore_type(movie):
    movie = Movie("Moana", 2016)
    with pytest.raises(ValueError):
        movie.metascore = 93.3
