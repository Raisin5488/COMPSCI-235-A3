import pytest
from movie_web_app.domain.review import Review


def test_1():
    name = Review("Moviename", "movie is v good", 8, "Banana")
    assert name.movie == "Moviename"
    assert name.review_text == "movie is v good"
    assert name.rating == 8
    assert name.user == "Banana"


def test_2():
    name = Review(123, 123, -8, "Banana")
    assert name.movie == ""
    assert name.review_text == ""
    assert name.rating is None
    assert name.user == "Banana"


def test_3():
    name = Review("name", "ok", "aFS", "Banana")
    assert name.rating is None


def test_4():
    name1 = Review("Moviename", "movie is v good", 8, "Banana")
    name2 = Review("Moviename", "movie is v good", 8, "Banana")
    assert name1 == name1
    assert name1 == name2


def test_5():
    name = Review("Moviename", "movie is v good", 8, "Banana")
    assert name.__repr__() == f"Moviename\nmovie is v good\n8\n{name.timestamp}"
