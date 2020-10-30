from sqlalchemy import (
    Table, MetaData, Column, Integer, REAL, String, Date, DateTime,
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
    Column('director_id', ForeignKey('directors.id')),
    Column('runtime_minutes', Integer, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('votes', Integer, nullable=False),
    Column('revenue_millions', REAL, nullable=False),
    Column('metascore', Integer, nullable=False),
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
    'watchLists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey("users.id")),
)


movies_actors = Table(
    'movies_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movies_id', ForeignKey("movies.id")),
    Column('actors_id', ForeignKey("actors.id")),
)

movies_genres = Table(
    'movies_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movies_id', ForeignKey("movies.id")),
    Column('genres_id', ForeignKey("genres.id")),
)

watchLists_movies = Table(
    'watchLists_movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('watchLists_id', ForeignKey('watchLists.id')),
    Column('movies_id', ForeignKey('movies.id'))
)


def map_model_to_tables():
    movies_mapper = mapper(Movie, movies, properties={
        'title': movies.c.title,
        'year': movies.c.year,
        'description': movies.c.description,
        'runtime_minutes': movies.c.runtime_minutes,
        'director': relationship(Director, back_populates='movies'),
        'actors': relationship(Actor, secondary=movies_actors, backref='movies'),
        'genres': relationship(Genre, secondary=movies_genres, backref='movies'),
        'rating': movies.c.rating,
        'votes': movies.c.votes,
        'revenue_millions': movies.c.revenue_millions,
        'metascore': movies.c.metascore,
    })
    mapper(User, users, properties={
        'username': users.c.username,
        'password': users.c.password,
        'time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        'reviews': relationship(Review, back_populates="user"),
    })
    # 'watch_list': relationship(WatchList)
    mapper(Director, directors, properties={
        'director_full_name': directors.c.director_full_name,
        'movies': relationship(Movie, back_populates='director')
    })
    mapper(Actor, actors, properties={
        'actor_full_name': actors.c.actor_full_name,
        # 'movies': relationship(movies_mapper, secondary=movies_actors, backref='actors')
    })
    mapper(Genre, genres, properties={
        'genre_name': genres.c.genre_name,
        # 'movies': relationship(movies_mapper, secondary=movies_genres, backref='genres')
    })

    mapper(Review, reviews, properties={
        # 'movie': relationship(Movie, ),
        'review_text': reviews.c.review_text,
        'rating': reviews.c.rating,
        'timestamp': reviews.c.timestamp,
        'user': relationship(User, back_populates="reviews"),
    })
    mapper(WatchList, watchLists, properties={
        # 'user_id': relationship(User, back_populates="watchList"),
        # 'movie_id': relationship(Movie, back_populates="watchList"),
    })
