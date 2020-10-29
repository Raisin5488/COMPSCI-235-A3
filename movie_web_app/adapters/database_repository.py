import csv
import os
import sqlite3
from abc import ABC

from sqlalchemy import engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from movie_web_app.adapters.movieFileCSVReader import MovieFileCSVReader
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.director import Director
from movie_web_app.domain.movie import Movie
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


def populate(engine: Engine, data_path):
    filename = "movie_web_app/adapters/Data1000Movies.csv"
    movie_file_reader = MovieFileCSVReader(filename)
    conn = engine.raw_connection()
    cursor = conn.cursor()
    temp_id = 1
    for director in movie_file_reader.dataset_of_directors:
        insert_directors = """
                INSERT INTO directors (
                id, director_full_name)
                VALUES (?, ?)"""
        cursor.execute(insert_directors, [temp_id, director.get_director()])
        temp_id += 1
    temp_id = 1
    for movie in movie_file_reader.dataset_of_movies:
        insert_movies = """
                INSERT INTO movies (
                id, title, year, description, director)
                VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(insert_movies, [temp_id, movie.get_title(), movie.get_year(), movie.description, movie.director.get_director()])
        temp_id += 1
    conn.commit()
    conn.close()


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
        connection = sqlite3.connect("movie-web.db")
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM movies WHERE title == '{title}' and year == '{year}'")
        temp = cursor.fetchall()
        connection.close()
        temp = temp[0]
        movie = Movie(temp[1], temp[2])
        movie.description = temp[3]
        movie.director = temp[4]
        return movie
