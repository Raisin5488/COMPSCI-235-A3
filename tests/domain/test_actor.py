import pytest
from movie_web_app.domain.actor import Actor


def test_1():
    actor = Actor(123)
    assert actor.actor_full_name is None


def test_2():
    actor = Actor("123")
    assert actor.actor_full_name == "123"
    assert actor.__repr__() == "<Actor 123>"


def test_3():
    actor = Actor("  123  ")
    assert actor.actor_full_name == "123"
    assert actor.__repr__() == "<Actor 123>"


def test_4():
    actor = Actor("Banana")
    assert actor.actor_full_name == "Banana"
    assert actor.__repr__() == "<Actor Banana>"


def test_5():
    actor1 = Actor("Banana")
    actor2 = Actor("Banana")
    assert actor1 == actor2


def test_6():
    actor1 = Actor("Banana")
    actor2 = Actor("banana")
    assert actor1 != actor2


def test_7():
    actor1 = Actor(123)
    actor2 = Actor(321)
    assert actor1 == actor2


def test_8():
    actor1 = Actor("Apple")
    actor2 = Actor("Banana")
    actor3 = Actor("Pear")
    list = [actor3, actor1, actor2]
    list.sort()
    assert list == [actor1, actor2, actor3]


def test_8():
    actor1 = Actor("Apple")
    actor2 = Actor("Banana")
    actor1.add_actor_colleague(actor2)
    assert actor1.check_if_this_actor_worked_with(actor2)
    assert not actor2.check_if_this_actor_worked_with(actor1)

