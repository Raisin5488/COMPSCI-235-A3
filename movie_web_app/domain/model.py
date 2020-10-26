from typing import Iterable


class Person:
    def __init__(self, id_number: int, firstname: str, lastname: str):
        self._id_number = id_number
        self._firstname = firstname
        self._lastname = lastname

    @property
    def id_number(self) -> int:
        return self._id_number

    @property
    def firstname(self) -> str:
        return self._firstname

    @property
    def lastname(self) -> str:
        return self._lastname


class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._comments = list()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self._comments)

    def add_comment(self, comment: 'Comment'):
        self._comments.append(comment)

    def __repr__(self) -> str:
        return f'<User {self._username} {self._password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username
