from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director
from movie_web_app.domain.genre import Genre


class Movie:

    def __init__(self, title: str, year: int):
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()
        if type(year) is not int:
            self.__year = None
        elif year < 1900:
            self.__year = None
        else:
            self.__year = year
        self.__description = ""
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = 0
        self.__rating = 0
        self.__votes = 0
        self.__revenue_millions = 0
        self.__metascore = 0

    @property
    def title(self) -> str:
        return self.__title

    @property
    def year(self) -> int:
        return self.__year

    @property
    def description(self) -> str:
        return self.__description

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self) -> [Actor]:
        return self.__actors

    @property
    def genres(self) -> [Genre]:
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @property
    def rating(self):
        return self.__rating

    @property
    def votes(self):
        return self.__votes

    @property
    def revenue_millions(self):
        return self.__revenue_millions

    @property
    def metascore(self):
        return self.__metascore

    @description.setter
    def description(self, description: str):
        if type(description) is not str:
            return
        else:
            self.__description = description.strip()

    @director.setter
    def director(self, director: Director):
        if type(director) is not Director:
            return
        else:
            self.__director = director

    @actors.setter
    def actors(self, new_actors):
        if type(new_actors) is not list:
            return
        for i in new_actors:
            if type(i) is not Actor:
                return
        self.__actors = new_actors

    @genres.setter
    def genres(self, genres):
        if type(genres) is not list:
            return
        for i in genres:
            if type(i) is not Genre:
                return
        self.__genres = genres

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes: int):
        if type(runtime_minutes) is not int:
            raise ValueError
        elif runtime_minutes < 0:
            raise ValueError
        self.__runtime_minutes = runtime_minutes

    @rating.setter
    def rating(self, rating):
        if type(rating) is not float:
            raise ValueError
        elif rating < 0 or rating > 10:
            raise ValueError
        self.__rating = rating

    @votes.setter
    def votes(self, votes):
        if type(votes) is not int:
            raise ValueError
        elif votes < 0:
            raise ValueError
        self.__votes = votes

    @revenue_millions.setter
    def revenue_millions(self, revenue_millions):
        if type(revenue_millions) is not float:
            raise ValueError
        elif revenue_millions < 0:
            raise ValueError
        self.__revenue_millions = revenue_millions

    @metascore.setter
    def metascore(self, metascore):
        if type(metascore) is not int:
            raise ValueError
        elif metascore < 0 or metascore > 100:
            raise ValueError
        self.__metascore = metascore

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__year}>"

    def __eq__(self, other):
        if self.title == other.title and self.year == other.year:
            return True
        return False

    def __lt__(self, other):
        if self.title == other.title:
            return self.year < other.year
        return self.title < other.title

    def __hash__(self):
        if self.title is None:
            if self.year is None:
                return 0
            else:
                return hash(str(self.year))
        else:
            if self.year is None:
                return hash(str(self.title))
            else:
                return hash(self.title + str(self.year))

    def add_actor(self, actor: Actor):
        if type(actor) is not Actor:
            return
        else:
            self.actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def add_genre(self, genre: Genre):
        if type(genre) is not Genre:
            return
        else:
            self.genres.append(genre)

    def remove_genre(self, genre: Genre):
        if genre in self.genres:
            self.genres.remove(genre)
