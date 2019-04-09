from datetime import datetime
from datetime import date


class Highscoreentry:
    date = 0
    name = ""
    point = 0

    def __init__(self, date, name, point):
        self.date = date
        self.name = name
        self.point = point

    def __repr__(self):
        return str(self.point)


class Highscorelist:
    def __init__(self):
        self.highscores = []

    def add_entry(self, entry):
        self.highscores.append(entry)
        self.highscores[10:20] = []
        print(self.highscores)


highscorelist = Highscorelist()
today = date.today()
for i in range(20):
    x = Highscoreentry(today, "Florian", i)
    highscorelist.add_entry(x)
