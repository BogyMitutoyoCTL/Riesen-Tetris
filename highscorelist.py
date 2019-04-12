from datetime import datetime
from datetime import date
import pickle
from Score import *


class Highscoreentry:
    date = 0
    name = ""
    point = 0

    def __init__(self, date: datetime.date, name: str, point: int):
        self.date = date  # type: datetime.date
        self.name = name
        self.point = point

    def __repr__(self):
        return str(self.point) + " " + self.name + " " + self.date.strftime("%d.%m.%y")

    def __gt__(self, other):
        return self.point > other.point

    def __lt__(self, other):
        return self.point < other.point


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
        with open(self.filename, 'rb') as f:
            temporary_list = pickle.load(f)
            self.highscores = temporary_list.highscores
score = Score()
y = str(score.points)

if __name__ == "__main__":
    tetrishighscores = Highscorelist('tetrisscores')
    print(score)

    today = date.today()
    x = Highscoreentry(today, "Domenik", y)
    tetrishighscores.add_entry(x)

    tetrishighscores.save()
    print(tetrishighscores.highscores)

    x = Highscorelist('tetrisscores')
    x.load()
    print(x.highscores)
