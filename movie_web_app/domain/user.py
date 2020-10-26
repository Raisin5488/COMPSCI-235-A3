from movie_web_app.domain.watchList import WatchList


class User:
    def __init__(self, username: str, password: str):
        self.__username = username.strip().lower()
        self.__password = password
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0
        self.__watch_list = WatchList()


    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    @property
    def watch_list(self) -> WatchList:
        return self.__watch_list

    def __repr__(self):
        return "<User {}>".format(self.user_name)

    def __eq__(self, other):
        if self.user_name == other.user_name:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)

    def watch_movie(self, movie):
        self.watched_movies.append(movie)
        self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        self.reviews.append(review)

    def get_watch_list(self):
        return self.watch_list

    def add_runtime(self, time):
        self.__time_spent_watching_movies_minutes += time
