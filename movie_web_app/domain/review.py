from datetime import datetime
from movie_web_app.domain.movie import Movie


class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int, user: str):
        if type(movie) is not Movie:
            self.movie = ""
        else:
            self.movie = movie
        if type(review_text) is not str:
            self.review_text = ""
        else:
            self.review_text = review_text
        if type(rating) is not int:
            self.rating = None
        elif rating < 0 or rating > 10:
            self.rating = None
        else:
            self.rating = rating
        self.timestamp = datetime.now()
        self.user = user

    def __repr__(self):
        return "{}\n{}\n{}\n{}".format(str(self.movie), self.review_text, str(self.rating), self.timestamp)

    def __eq__(self, other):
        if self.movie == other.movie:
            if self.review_text == other.review_text:
                if self.rating == other.rating:
                    if self.timestamp == other.timestamp:
                        return True
        return False
