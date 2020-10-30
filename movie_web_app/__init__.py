import os

from flask import Flask, request, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import NullPool

import movie_web_app.adapters.repository as repo
from movie_web_app.domain.model import Person
from movie_web_app.adapters.movieFileCSVReader import MovieFileCSVReader
from movie_web_app.adapters.orm import metadata, map_model_to_tables
from movie_web_app.adapters import database_repository


def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_object('config.Config')
    data_path = os.path.join('movie_web_app', 'adapters', 'data')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository instance for a memory-based repository.
        repo.repo_instance = MovieFileCSVReader("movie_web_app/adapters/Data1000Movies.csv")

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=database_echo)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_repository.populate(database_engine, data_path)

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    with app.app_context():
        from .movie_blueprint import movie
        app.register_blueprint(movie.movie_blueprint)
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
    return app
