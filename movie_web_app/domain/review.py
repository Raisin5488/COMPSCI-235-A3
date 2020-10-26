from datetime import datetime
from movie_web_app.domain.movie import Movie


class Review:
    def __init__(self, movie: str, review_text: str, rating: int, user: str):
        if type(movie) is not str:
            self.__movie = ""
        else:
            self.__movie = movie
        if type(review_text) is not str:
            self.__review_text = ""
        else:
            self.__review_text = review_text
        if type(rating) is not int:
            self.__rating = None
        elif rating < 0 or rating > 10:
            self.__rating = None
        else:
            self.__rating = rating
        self.__timestamp = datetime.now()
        self.__user = user

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def user(self):
        return self.__user

    def __repr__(self):
        return "{}\n{}\n{}\n{}".format(str(self.movie), self.review_text, str(self.rating), self.timestamp)

    def __eq__(self, other):
        if self.movie == other.movie:
            if self.review_text == other.review_text:
                if self.rating == other.rating:
                    if self.timestamp == other.timestamp:
                        return True
        return False
