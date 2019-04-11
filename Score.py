import time

from numbersforwatch import number_pixels, Number
from field import Field
from painter import Led_Matrix_Painter




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


if __name__ == "__main__":
    score = Score()

    led_matrix_painter = Led_Matrix_Painter()
    scoreboard = Field(32, 8)
    while True:



            text = "0000" + str(score.point)
            text = text[-5:]

            for x in range(len(text)):
                n = Number(int(text[x]))
                scoreboard.set_block(n.block, x*5, 2)

            led_matrix_painter.draw(scoreboard)
            time.sleep(0.1)


            score.score_for_line(4)
            scoreboard.set_all_pixels_to_black()


