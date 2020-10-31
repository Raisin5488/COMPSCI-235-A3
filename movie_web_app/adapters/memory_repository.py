import csv
from abc import ABC

from movie_web_app.adapters.movieFileCSVReader import MovieFileCSVReader
from movie_web_app.domain.movie import Movie
from movie_web_app.domain.review import Review
from movie_web_app.domain.user import User
from movie_web_app.adapters.repository import AbstractRepository


def fuzzy_search(compare, set_string):
    set_string = set_string.lower()
    compare = compare.lower()

    if remove_letters(compare, set_string):
        return True
    elif swap_letters(compare, set_string):
        return True
    elif add_letters(compare, set_string):
        return True
    else:
        return False


def get_letters():
    temp_list = [" "]
    for i in range(97, 123):
        temp_list.append(chr(i))
    return temp_list


def remove_letters(compare, set_string):
    for i in range(1, len(compare)):
        if compare[:i - 1] in set_string and compare[i:] in set_string:
            return True
    return False


def swap_letters(compare, set_string):
    if compare == set_string:
        return True
    for i in range(0, len(compare) - 1):
        temp = compare[:i] + compare[i + 1] + compare[i] + compare[i + 2:]
        if temp in set_string:
            return True
    return False


def add_letters(compare, set_string):
    if compare == set_string:
        return True
    temp_list = get_letters()
    for i in temp_list:
        for j in range(0, len(compare) + 1):
            temp = compare[:j] + i + compare[j:]
            if temp in set_string:
                return True
    return False


class MemoryRepository(AbstractRepository):

    def __init__(self, file_name: str):
        movie_reader = MovieFileCSVReader(file_name)
        self.__file_name = file_name
        self.dataset_of_movies = movie_reader.dataset_of_movies
        self.__dataset_of_actors = movie_reader.dataset_of_actors
        self.__dataset_of_directors = movie_reader.dataset_of_directors
        self.__dataset_of_genres = movie_reader.dataset_of_genres
        self._users = []
        self._reviews = []

    def get_movie_title(self, movie_title: str):
        return_list = []
        if len(movie_title) <= 5:
            for movie in self.dataset_of_movies:
                if movie_title.lower() in movie.title.lower():
                    return_list.append(movie)
        else:
            for movie in self.dataset_of_movies:
                if fuzzy_search(movie_title, movie.title):
                    return_list.append(movie)
        if not return_list:
            return None
        else:
            return return_list

    def get_director_name(self, director_to_find: str):
        return_list = []
        for movie in self.dataset_of_movies:
            if fuzzy_search(director_to_find, movie.director.director_full_name):
                return_list.append(movie)
        if not return_list:
            return None
        else:
            return return_list

    def get_actor_name(self, actor_to_find: str):
        return_list = []
        for movie in self.dataset_of_movies:
            for actor in movie.actors:
                if fuzzy_search(actor_to_find, actor.actor_full_name):
                    return_list.append(movie)
        if not return_list:
            return None
        else:
            return return_list

    def get_genre_name(self, genre_to_find: str):
        return_list = []
        for movie in self.dataset_of_movies:
            for genre in movie.genres:
                if fuzzy_search(genre_to_find, genre.genre_name):
                    return_list.append(movie)
        if not return_list:
            return None
        else:
            return return_list

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def get_exact_movie(self, title: str, year: int):
        for movie in self.dataset_of_movies:
            if movie.title == title and movie.year == year:
                return movie
        return None

    def get_reviews(self):
        return self._reviews

    def add_review(self, movie: Movie, review_text: str, rating: int, username: str):
        for i in self._users:
            if i.username == username:
                self._reviews.append(Review(movie, review_text, rating, i))

    def get_movies(self):
        return self.dataset_of_movies
