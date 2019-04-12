import time

from numbersforwatch import Number
from field import Field
from painter import Led_Matrix_Painter


class Score:
    def __init__(self, field_for_score: Field):
        self.points = 0
        self.field_for_score = field_for_score

    def score_for_line(self, deleted_lines):
        if deleted_lines == 1:
            self.points += 10
        elif deleted_lines == 2:
            self.points += 40
        elif deleted_lines == 3:
            self.points += 90
        elif deleted_lines == 4:
            self.points += 200

    def score_for_block(self):
        self.points += 1

    def get_score(self) -> str:
        return ("0000"+str(self.points))[-5:]

    def draw_score_on_field(self):
        text = ("0000" + str(self.points))[-5:]

        for x in range(len(text)):
            n = Number(int(text[x]))
            self.field_for_score.set_block(n.block, x*5, 2)


if __name__ == "__main__":
    score = Score()

    led_matrix_painter = Led_Matrix_Painter()
    scoreboard = Field(32, 8)
    while True:
            text = ("0000" + str(score.points))[-5:]

            for x in range(len(text)):
                n = Number(int(text[x]))
                scoreboard.set_block(n.block, x*5, 2)

            led_matrix_painter.draw(scoreboard)
            time.sleep(0.1)

            score.score_for_line(4)
            scoreboard.set_all_pixels_to_black()


