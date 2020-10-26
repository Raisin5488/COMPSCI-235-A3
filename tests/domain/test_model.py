import pytest
from movie_web_app.domain.model import Person, User


def test_1():
    name = Person(123, "Apple", "Banana")
    assert name.id_number == 123
    assert name.firstname == "Apple"
    assert name.lastname == "Banana"


def test_2():
    name = User("Banana", "abcd1234")
    assert name.username == "Banana"
    assert name.password == "abcd1234"
    assert name.__repr__() == "<User Banana abcd1234>"


def test_3():
    name1 = User("Banana", "abcd1234")
    name2 = User("Apple", "abcd1234")
    name3 = User("Banana", "1234abcd")
    name4 = 123
    assert name1 != name2
    assert name1 == name3
    assert name1 != name4
