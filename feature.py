from painter import RGB_Field_Painter
from highscorelist import *


class Feature:
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter, highscorelist: Highscorelist = Highscorelist("Not_used")):
        self.mode = 0
        self.field_leds = field_leds
        self.field_matrix = field_matrix
        self.rgb_field_painter = rgb_field_painter
        self.led_matrix_painter = led_matrix_painter
        self.highscorelist = highscorelist
        self.playername = ""
        self.game_over = True

    def event(self, eventname: str):
        raise NotImplementedError

    def tick(self):
        raise NotImplementedError

    def start(self, playername: str = None):
        self.playername = playername

    def stop(self):
        raise NotImplementedError

    def is_game_over(self) -> bool:
        return self.game_over
