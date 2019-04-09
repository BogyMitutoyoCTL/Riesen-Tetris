from datetime import datetime
from datetime import date
from typing import *

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
    def __init__(self):
        self.highscores = []

    def add_entry(self, entry: Highscoreentry):
        self.highscores.append(entry)
        self.highscores.sort(reverse=True)
        self.highscores[10:20] = []


highscorelist = Highscorelist()
today = date.today()
print(today)
for i in range(20):
    x = Highscoreentry(today, "Florian", i)
    highscorelist.add_entry(x)
print(highscorelist.highscores)
