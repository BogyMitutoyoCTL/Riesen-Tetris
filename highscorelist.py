import pickle
from datetime import datetime


class Highscoreentry:
    def __init__(self, date: datetime.date, name: str, point: int):
        self.date = date  # type: datetime.date
        self.name = name
        self.points = point

    def __repr__(self):
        return str(self.points) + " " + self.name + " " + self.date.strftime("%d.%m.%y")

    def __gt__(self, other):
        return self.points > other.points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.points == other.points

    def __ge__(self, other):
        return self.points >= other.points


class Highscorelist:
    def __init__(self, filename):
        self.highscores = []
        self.filename = filename

    def add_entry(self, entry: Highscoreentry):
        self.highscores.append(entry)
        self.highscores.sort(reverse=True)
        self.highscores[10:20] = []

    def save(self, ):
        with open(self.filename, 'wb') as f:
            pickle.dump(self, f)

    def load(self):
        try:
            with open(self.filename, 'rb') as f:
                temporary_list = pickle.load(f)
                self.highscores = temporary_list.highscores
        except FileNotFoundError:
            pass
