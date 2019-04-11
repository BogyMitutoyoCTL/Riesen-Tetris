
class Score:
    def __init__(self):
        self.point = 0
    def score_for_line(self, deleted_lines):
        score.score_for_line(deleted_lines)
        pass


    def score_for_block(self):
        self.point +=1







score = Score()
assert(score.point == 0)
score.score_for_block()
assert (score.point ==1)
score.score_for_line(0)
assert (score.point ==1)
score.score_for_line(1)
assert (score.point ==11)
score.score_for_line(2)
assert (score.point == 51)
score.score_for_line(3)
assert (score.point ==1 41)
score.score_for_line(4)
assert (score.point == 341)