import csv
from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director
from movie_web_app.domain.genre import Genre
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
    list = [" "]
    for i in range(97, 123):
        list.append(chr(i))
    return list


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
    list = get_letters()
    for i in list:
        for j in range(0, len(compare) + 1):
            temp = compare[:j] + i + compare[j:]
            if temp in set_string:
                return True
    return False


class MovieFileCSVReader(AbstractRepository):

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = []
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()

        self.__total_runtime_minutes = 0
        self.__runtime_minutes_number_of_movies = 0
        self.__total_rating = 0
        self.__rating_number_of_movies = 0
        self.__total_votes = 0
        self.__votes_number_of_movies = 0
        self.__total_revenue_millions = 0
        self.__revenue_millions_number_of_movies = 0
        self.__total_metascore = 0
        self.__metascore_number_of_movies = 0
        self.read_csv_file()

        self._users = []
        self._reviews = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                movie = Movie(row["Title"], int(row["Year"]))
                movie.description = row["Description"]
                movie.runtime_minutes = int(row["Runtime (Minutes)"])
                self.__total_runtime_minutes += int(row["Runtime (Minutes)"])
                self.__runtime_minutes_number_of_movies += 1
                if row["Rating"] != "N/A":
                    movie.rating = float(row['Rating'])
                    self.__total_rating += float(row['Rating'])
                    self.__rating_number_of_movies += 1
                if row["Votes"] != "N/A":
                    movie.votes = int(row["Votes"])
                    self.__total_votes += int(row["Votes"])
                    self.__votes_number_of_movies += 1
                if row["Revenue (Millions)"] != "N/A":
                    movie.revenue_millions = float(row["Revenue (Millions)"])
                    self.__total_revenue_millions += float(row["Revenue (Millions)"])
                    self.__revenue_millions_number_of_movies += 1
                if row["Metascore"] != "N/A":
                    movie.metascore = int(row["Metascore"])
                    self.__total_metascore += int(row["Metascore"])
                    self.__metascore_number_of_movies += 1
                movie.director = Director(row["Director"])
                self.__dataset_of_directors.add(Director(row["Director"]))
                for actor in row["Actors"].split(","):
                    movie.add_actor(Actor(actor.strip()))
                    self.__dataset_of_actors.add(Actor(actor.strip()))
                for genre in row["Genre"].split(","):
                    movie.add_genre(Genre(genre.strip()))
                    self.__dataset_of_genres.add(Genre(genre.strip()))
                index += 1
                self.__dataset_of_movies.append(movie)

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    def calculate_average_runtime(self):
        return round(self.__total_runtime_minutes / self.__runtime_minutes_number_of_movies)

    def calculate_average_rating(self):
        return round(self.__total_rating / self.__rating_number_of_movies, 1)

    def calculate_average_votes(self):
        return round(self.__total_votes / self.__votes_number_of_movies)

    def calculate_average_revenue_millions(self):
        return round(self.__total_revenue_millions / self.__revenue_millions_number_of_movies, 2)

    def calculate_average_metascore(self):
        return round(self.__total_metascore / self.__metascore_number_of_movies)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self.__dataset_of_movies):
            raise StopIteration
        else:
            self._current += 1
            return self.__dataset_of_movies[self._current-1]

    def get_movie_title(self, movie_title: str):
        return_list = []
        if len(movie_title) <= 5:
            for movie in self.__dataset_of_movies:
                if movie_title.lower() in movie.title.lower():
                    return_list.append(movie)
        else:
            for movie in self.__dataset_of_movies:
                if fuzzy_search(movie_title, movie.title):
                    return_list.append(movie)
        if not return_list:
            return None
        else:
            return return_list

    def get_director_name(self, director_to_find: str):
        return_list = []
        for movie in self.__dataset_of_movies:
            if fuzzy_search(director_to_find, movie.director.director_full_name):
                return_list.append(movie)
        if not return_list:
            return None
        else:
            return return_list

    def get_actor_name(self, actor_to_find: str):
        return_list = []
        for movie in self.__dataset_of_movies:
            for actor in movie.actors:
                if fuzzy_search(actor_to_find, actor.actor_full_name):
                    return_list.append(movie)
        if not return_list:
            return None
        else:
            return return_list

    def get_genre_name(self, genre_to_find: str):
        return_list = []
        for movie in self.__dataset_of_movies:
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
        for movie in self.__dataset_of_movies:
            if movie.title == title and movie.year == year:
                return movie
        return None

    def get_reviews(self):
        return self._reviews

    def add_review(self, movie: str, review_text: str, rating: int, user: str):
        self._reviews.append(Review(movie, review_text, rating, user))
