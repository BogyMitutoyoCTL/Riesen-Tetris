class Score:
    def __init__(self):
        self.point = 0

    def score_for_line(self, deleted_lines):
        if deleted_lines == 1:
            self.point += 10
        elif deleted_lines == 2:
            self.point += 40
        elif deleted_lines == 3:
            self.point += 90
        elif deleted_lines >= 4:
            self.point += 200

    def score_for_block(self):
        self.point += 1


score = Score()
assert (score.point == 0)
score.score_for_block()
assert (score.point == 1)
score.score_for_line(0)
assert (score.point == 1)
score.score_for_line(1)
assert (score.point == 11)
score.score_for_line(2)
assert (score.point == 51)
score.score_for_line(3)
assert (score.point == 141)
score.score_for_line(4)
assert (score.point == 341)

