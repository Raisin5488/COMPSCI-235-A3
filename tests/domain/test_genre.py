import pytest
from movie_web_app.domain.genre import Genre


def test_1():
    name = Genre(123)
    assert name.genre_name is None


def test_2():
    name = Genre("123")
    assert name.genre_name == "123"
    assert name.__repr__() == "<Genre 123>"


def test_3():
    name = Genre("  123  ")
    assert name.genre_name == "123"
    assert name.__repr__() == "<Genre 123>"


def test_4():
    name = Genre("Banana")
    assert name.genre_name == "Banana"
    assert name.__repr__() == "<Genre Banana>"


def test_5():
    name1 = Genre("Banana")
    name2 = Genre("Banana")
    assert name1 == name2


def test_6():
    name1 = Genre("Banana")
    name2 = Genre("banana")
    assert name1 != name2


def test_7():
    name1 = Genre(123)
    name2 = Genre(321)
    assert name1 == name2


def test_8():
    name1 = Genre("Apple")
    name2 = Genre("Banana")
    name3 = Genre("Pear")
    list = [name3, name1, name2]
    list.sort()
    assert list == [name1, name2, name3]



