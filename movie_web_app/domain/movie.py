from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director
from movie_web_app.domain.genre import Genre


class Movie:

    def __init__(self, title: str, year: int):
        if title == "" or type(title) is not str:
            self.title = None
        else:
            self.title = title.strip()
        if type(year) is not int:
            self.year = None
        elif year < 1900:
            self.year = None
        else:
            self.year = year
        self.description = ""
        self.director = None
        self.actors = []
        self.genres = []
        self.runtime_minutes = 0
        self.rating = 0
        self.votes = 0
        self.revenue_millions = 0
        self.metascore = 0

    def get_title(self):
        return self.title

    def get_year(self):
        return self.year

    def get_director(self):
        return self.director

    def __repr__(self):
        return f"<Movie {self.title}, {self.year}>"

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
