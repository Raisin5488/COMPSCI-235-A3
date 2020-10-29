class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.genre_name = None
        else:
            self.genre_name = genre_name.strip()

    def __repr__(self):
        return f"<Genre {self.genre_name}>"

    def __eq__(self, other):
        if self.genre_name == other.genre_name:
            return True
        return False

    def __lt__(self, other):
        return self.genre_name < other.genre_name

    def __hash__(self):
        return hash(self.genre_name)
