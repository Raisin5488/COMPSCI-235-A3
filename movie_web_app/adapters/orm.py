from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director
from movie_web_app.domain.genre import Genre
from movie_web_app.domain.movie import Movie
from movie_web_app.domain.review import Review
from movie_web_app.domain.user import User
from movie_web_app.domain.watchList import WatchList


metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, nullable=False),
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(255), nullable=False),
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('director_full_name', String(255), nullable=False),
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(255), nullable=False),
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('year', Integer, nullable=False),
    Column('description', String(255), nullable=False),
    Column('director_id', ForeignKey("directors.id")),
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey("movies.id")),
    Column('review_text', String(255), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('user_id', ForeignKey("users.id")),
)


watchLists = Table(
    'watchList', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
)


def map_model_to_tables():
    mapper(User, users, properties={
        'username': users.c.username,
        'password': users.c.password,
    })
    mapper(Actor, actors, properties={
        'actor_full_name': actors.c.actor_full_name,
    })
    mapper(Director, directors, properties={
        'director_full_name': directors.c.director_full_name,
    })
    mapper(Genre, genres, properties={
        'genre_name': genres.c.genre_name,
    })
    mapper(Movie, movies, properties={
        'title': movies.c.title,
        'year': movies.c.year,
        'description': movies.c.description,
        'director': relationship(Director, backref="movie"),
    })
    mapper(Review, reviews, properties={
        'movie': relationship(Movie, backref="review"),
        'review_text': reviews.c.review_text,
        'rating': reviews.c.rating,
        'timestamp': reviews.c.timestamp,
        'user': relationship(User, backref="review"),
    })
