import csv
from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director
from movie_web_app.domain.genre import Genre
from movie_web_app.domain.movie import Movie


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.dataset_of_movies = []
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

    def read_csv_file_movies(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            self.dataset_of_movies = []
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                movie = Movie(row["Title"], int(row["Year"]))
                movie.description = row["Description"]
                movie.runtime_minutes = int(row["Runtime (Minutes)"])
                if row["Rating"] != "N/A":
                    movie.rating = float(row['Rating'])
                if row["Votes"] != "N/A":
                    movie.votes = int(row["Votes"])
                if row["Revenue (Millions)"] != "N/A":
                    movie.revenue_millions = float(row["Revenue (Millions)"])
                if row["Metascore"] != "N/A":
                    movie.metascore = int(row["Metascore"])
                for director in self.__dataset_of_directors:
                    if director.director_full_name == row["Director"]:
                        movie.director = director

                temp_actor_list = []
                for actor in row["Actors"].split(","):
                    temp_actor_list.append(actor.strip())

                temp_genre_list = []
                for genre in row["Genre"].split(","):
                    temp_genre_list.append(genre.strip())

                for actor in self.__dataset_of_actors:
                    if actor.actor_full_name in temp_actor_list:
                        movie.add_actor(actor)

                for genre in self.__dataset_of_genres:
                    if genre.genre_name in temp_genre_list:
                        movie.add_genre(genre)
                index += 1
                self.dataset_of_movies.append(movie)

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
                self.dataset_of_movies.append(movie)

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
        if self._current >= len(self.dataset_of_movies):
            raise StopIteration
        else:
            self._current += 1
            return self.dataset_of_movies[self._current-1]
