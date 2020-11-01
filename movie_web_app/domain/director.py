class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.director_full_name = None
        else:
            self.director_full_name = director_full_name.strip()
        self.movies = []

    def get_director(self):
        return self.director_full_name

    def __repr__(self):
        return f"<Director {self.get_director()}>"

    def __eq__(self, other):
        if self.director_full_name == other.director_full_name:
            return True
        return False

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.director_full_name)
