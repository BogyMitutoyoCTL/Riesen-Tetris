from datetime import datetime
from datetime import date
import pickle


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


if __name__ == "__main__":
    snakehighscores = Highscorelist('snakescores')
    snakehighscores.save()
    tetrishighscores = Highscorelist('tetrisscores')

    today = date.today()
    print(today)
    for i in range(20):
        x = Highscoreentry(today, "Florian", i)
        tetrishighscores.add_entry(x)
    tetrishighscores.save()
    tetrishighscores.save()
    print(tetrishighscores.highscores)

    x = Highscorelist('tetrisscores')
    x.load()
    print(x.highscores)
