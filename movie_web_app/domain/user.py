from movie_web_app.domain.watchList import WatchList


class User:
    def __init__(self, username: str, password: str):
        self.username = username.strip().lower()
        self.password = password
        self.watched_movies = []
        self.reviews = []
        self.time_spent_watching_movies_minutes = 0
        self.watch_list = WatchList()

    def __repr__(self):
        return "<User {}>".format(self.username)

    def __eq__(self, other):
        if self.username == other.user_name:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.username < other.user_name

    def __hash__(self):
        return hash(self.username)

    def watch_movie(self, movie):
        self.watched_movies.append(movie)
        self.time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        self.reviews.append(review)

    def get_watch_list(self):
        return self.watch_list

    def add_runtime(self, time):
        self.time_spent_watching_movies_minutes += time
