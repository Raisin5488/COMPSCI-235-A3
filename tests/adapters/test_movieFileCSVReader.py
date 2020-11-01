import pytest

from movie_web_app import MemoryRepository
from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director
from movie_web_app.domain.genre import Genre
from movie_web_app.domain.movie import Movie
from movie_web_app.adapters.movieFileCSVReader import MovieFileCSVReader


@pytest.fixture
def file_reader():
    file_reader = MovieFileCSVReader('movie_web_app/adapters/Data1000Movies.csv')
    file_reader.read_csv_file()
    return file_reader


@pytest.fixture
def memory_repository(file_reader):
    memory_repository = MemoryRepository('movie_web_app/adapters/Data1000Movies.csv')
    file_reader.read_csv_file()
    return memory_repository


def test_given(file_reader):
    assert len(file_reader.dataset_of_movies) == 1000
    assert len(file_reader.dataset_of_actors) == 1985
    assert len(file_reader.dataset_of_directors) == 644
    assert len(file_reader.dataset_of_genres) == 20


def test_other(file_reader):
    all_directors_sorted = sorted(file_reader.dataset_of_directors)
    assert all_directors_sorted[0:3] == [Director("Aamir Khan"), Director("Abdellatif Kechiche"), Director("Adam Leon")]


def test_average_runtime(file_reader):
    assert file_reader.calculate_average_runtime() == 113


def test_average_rating(file_reader):
    assert (file_reader.calculate_average_rating()) == 6.7


def test_average_votes(file_reader):
    assert (file_reader.calculate_average_votes()) == 169808


def test_average_revenue_millions(file_reader):
    assert (file_reader.calculate_average_revenue_millions()) == 82.96


def test_average_metascore(file_reader):
    assert (file_reader.calculate_average_metascore()) == 59


def test_movie_descriptopn(file_reader):
    assert file_reader.dataset_of_movies[0].description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."


def test_movie_runtime(file_reader):
    assert file_reader.dataset_of_movies[0].runtime_minutes == 121


def test_movie_rating(file_reader):
    assert file_reader.dataset_of_movies[0].rating == 8.1


def test_movie_votes(file_reader):
    assert file_reader.dataset_of_movies[0].votes == 757074


def test_movie_revenue(file_reader):
    assert file_reader.dataset_of_movies[0].revenue_millions == 333.13


def test_movie_metascore(file_reader):
    assert file_reader.dataset_of_movies[0].metascore == 76


def test_movie_revenue_NA(file_reader):
    assert file_reader.dataset_of_movies[7].revenue_millions == 0


def test_movie_metascore_NA(file_reader):
    assert file_reader.dataset_of_movies[25].metascore == 0


def test_movie_actor(file_reader):
    assert file_reader.dataset_of_movies[0].actors == [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper"), Actor("Zoe Saldana")]


def test_movie_genre(file_reader):
    assert file_reader.dataset_of_movies[0].genres == [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]


def test_movie_director(file_reader):
    print(type(file_reader.dataset_of_movies[0].director))
    print(type(Director("James Gunn")))
    assert file_reader.dataset_of_movies[0].director == Director("James Gunn")


def test_search_title_fuzzy0(memory_repository):
    assert memory_repository.get_movie_title("the avengers") == [Movie("The Avengers", 2012)]


def test_search_title_fuzzy1(memory_repository):
    assert memory_repository.get_movie_title("hee avengers") == [Movie("The Avengers", 2012)]


def test_search_title_fuzzy2(memory_repository):
    assert memory_repository.get_movie_title("te avengers") == [Movie("The Avengers", 2012)]


def test_search_title_fuzzy3(memory_repository):
    assert memory_repository.get_movie_title("the avengerss") == [Movie("The Avengers", 2012)]


def test_search_title_normal1(memory_repository):
    assert len(memory_repository.get_movie_title("pirat")) == 3


def test_search_director_fuzzy0(memory_repository):
    assert len(memory_repository.get_director_name("James Gunn")) == 3


def test_search_director_fuzzy1(memory_repository):
    assert len(memory_repository.get_director_name("JamesGunn")) == 3


def test_search_director_fuzzy2(memory_repository):
    assert len(memory_repository.get_director_name("Jaems Gunn")) == 3


def test_search_director_fuzzy3(memory_repository):
    assert len(memory_repository.get_director_name("James GGunn")) == 3


def test_search_actor_normal(memory_repository):
    assert len(memory_repository.get_actor_name("Robert Downey Jr.")) == 12


def test_search_genre_normal(memory_repository):
    assert len(memory_repository.get_genre_name("sci fi")) == 120
