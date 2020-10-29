import csv
import os
import sqlite3
from abc import ABC

from sqlalchemy import engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from movie_web_app.adapters.movieFileCSVReader import MovieFileCSVReader
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.director import Director
from movie_web_app.domain.movie import Movie
from movie_web_app.domain.review import Review
from movie_web_app.domain.user import User


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:

            movie_data = row
            movie_key = movie_data[0]

            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]

            number_of_tags = len(movie_data) - 6
            movie_tags = movie_data[-number_of_tags:]

            # Add any new tags; associate the current article with tags.
            for tag in movie_tags:
                if tag not in tags.keys():
                    tags[tag] = list()
                tags[tag].append(movie_key)

            del movie_data[-number_of_tags:]

            yield movie_data


def populate(session_factory, data_path):
    filename = "movie_web_app/adapters/Data1000Movies.csv"
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    # create a configured "Session" class
    Session = sessionmaker(bind=session_factory)

    # create a Session
    session = Session()

    # session = session_factory()

    # This takes all movies from the csv file (represented as domain model objects) and adds them to the
    # database. If the uniqueness of directors, actors, genres is correctly handled, and the relationships
    # are correctly set up in the ORM mapper, then all associations will be dealt with as well!
    for movie in movie_file_reader.dataset_of_movies:
        session.add(movie)
    session.commit()


class SessionContextManager:

    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_movies(self):
        all_movies = []
        try:
            all_movies = self._session_cm.session.query(Movie).all()
        except NoResultFound:
            print("No movies found in DB.")
            pass
        return all_movies

    def get_director_name(self, director_to_find):
        connection = sqlite3.connect("movie-web.db")
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM movies WHERE director == '{director_to_find}'")
        temp = cursor.fetchall()
        temp = temp[0]
        movie = Movie(temp[1], temp[2])
        movie.description = temp[3]
        movie.director = temp[4]
        return [movie]

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self.__dataset_of_movies):
            raise StopIteration
        else:
            self._current += 1
            return self.__dataset_of_movies[self._current - 1]

    def get_exact_movie(self, title, year):
        temp = self._session_cm.session.query(Movie).filter(Movie.title == title)
        return temp

    def get_movie_title(self, title):
        temp = self._session_cm.session.query(Movie).filter(Movie.title == title)
        return temp

    def get_actor_name(self, actor):
        temp = self._session_cm.session.query(Movie).filter(actor in Movie.actors)
        print(temp)
        return temp

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def get_reviews(self):
        return self._session_cm.session.query(Review).all()

    def add_review(self, movie: str, review_text: str, rating: int, user: str):
        user_to_add = self._session_cm.session.query(User).filter_by(username=user)
        review = Review(movie, review_text, rating, user_to_add)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()
