import pytest
from movie_web_app.domain.director import Director


def test_1():
    person = Director(123)
    assert person.director_full_name is None


def test_2():
    person = Director("123")
    assert person.director_full_name == "123"
    assert person.__repr__() == "<Director 123>"


def test_3():
    person = Director("  123  ")
    assert person.director_full_name == "123"
    assert person.__repr__() == "<Director 123>"


def test_4():
    person = Director("Banana")
    assert person.director_full_name == "Banana"
    assert person.__repr__() == "<Director Banana>"


def test_5():
    person1 = Director("Banana")
    person2 = Director("Banana")
    assert person1 == person2


def test_6():
    person1 = Director("Banana")
    person2 = Director("banana")
    assert person1 != person2


def test_7():
    person1 = Director(123)
    person2 = Director(321)
    assert person1 == person2


def test_8():
    person1 = Director("Apple")
    person2 = Director("Banana")
    person3 = Director("Pear")
    list = [person3, person1, person2]
    list.sort()
    assert list == [person1, person2, person3]



