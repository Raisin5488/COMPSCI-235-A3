import os
from abc import ABC

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from movie_web_app.adapters.movieFileCSVReader import MovieFileCSVReader
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.movie import Movie
from movie_web_app.domain.user import User


def populate(session_factory, data_path, data_filename):
    filename = os.path.join(data_path, data_filename)
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    session = session_factory()
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

    def get_articles(self):
        all_movies = []
        try:
            all_movies = self._session_cm.session.query(Movie).all()
        except NoResultFound:
            print("No movies found in DB.")
            pass
        return all_movies
