import time

from numbersforwatch import Number
from field import Field
from painter import Led_Matrix_Painter


class Score:
    def __init__(self):
        self.points = 0

    def score_for_line(self, deleted_lines):
        if 0 <= deleted_lines <= 4:
            self.points += [10, 40, 90, 200][deleted_lines]
        else:
            raise NotImplementedError

    def score_for_block(self):
        self.points += 1

    def get_score_str(self) -> str:
        return ("0000" + str(self.points))[-5:]

    def get_score_int(self) -> int:
        return self.points

    def draw_score_on_field(self, field_for_score: Field):
        position = 0
        for digit in self.get_score_str():
            number = Number(int(digit)).block
            field_for_score.set_block(number, position, 2)
            position += number.width
            position += 1  # 1 pixel space between digits


if __name__ == "__main__":
    score = Score()
    led_matrix_painter = Led_Matrix_Painter()
    scoreboard = Field(32, 8)
    while True:
        score.draw_score_on_field(scoreboard)
        led_matrix_painter.draw(scoreboard)
        time.sleep(0.1)

        score.score_for_line(4)
        scoreboard.set_all_pixels_to_black()
