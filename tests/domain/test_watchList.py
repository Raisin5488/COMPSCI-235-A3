import pytest
from movie_web_app.domain.movie import Movie
from movie_web_app.domain.watchList import WatchList


@pytest.fixture
def watchlist():
    return WatchList()


def test_given(watchlist):
    watchlist = WatchList()
    assert watchlist.size() == 0
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watchlist.first_movie_in_watchlist() == Movie("Moana", 2016)


def test_size(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watchlist.size() == 3


def test_add_same_movie(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.size() == 1


def test_remove_moive_not_in_list(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.remove_movie(Movie("Ice Age", 2002))
    assert watchlist.size() == 1


def test_remove_movie(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.remove_movie(Movie("Moana", 2016))
    assert watchlist.size() == 0


def test_select_movie_to_watch(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watchlist.select_movie_to_watch(2) == Movie("Guardians of the Galaxy", 2012)


def test_select_movie_out_of_range(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watchlist.select_movie_to_watch(3) is None


def test_iterator(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    temp = iter(watchlist)
    assert next(temp) == Movie("Moana", 2016)


def test_iterator_out_of_bound(watchlist):
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    temp = iter(watchlist)
    next(temp)
    next(temp)
    next(temp)
    with pytest.raises(StopIteration):
        next(temp)
