import abc
from typing import List

from movie_web_app.domain.user import User
from movie_web_app.domain.model import Person

repo_instance = None


class AbstractRepository(abc.ABC):
    pass


class PeopleRepository(AbstractRepository):
    def __init__(self, *args):
        self._people: List[Person] = list()
        self._users = list()

        for person in args:
            self._people.append(person)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._people):
            raise StopIteration
        else:
            self._current += 1
            return self._people[self._current-1]

    def get_person(self, person_id: int):
        return next((person for person in self._people if person.id_number == person_id), None)

    def get_person_firstname(self, firstname: str):
        return next((person for person in self._people if person.firstname == firstname), None)

    def get_person_lastname(self, lastname: str):
        return next((person for person in self._people if person.lastname == lastname), None)

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)
