from features.clock import Clock
from field import Field, BLACK
from painter import Led_Matrix_Painter, RGB_Field_Painter


class BinaryClock(Clock):

    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(BinaryClock, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

    def draw_block(self, x, y, color):
        self.field_leds.field[y][x] = color
        self.field_leds.field[y-1][x] = color
        self.field_leds.field[y][x+1] = color
        self.field_leds.field[y - 1][x+1] = color

    def draw_digit(self, number:int, position, color):
        for i in range(6):
            bright = (number & (2**i)) > 0
            if bright:
                self.draw_block(position, 19 - 3 * i, color)
            else:
                self.draw_block(position, 19 - 3 * i, [color[0] // 16, color[1] // 16, color[2] // 16])

    def draw_clock(self, color: list = None):
        hour, minute, second = self.get_time()
        self.draw_digit(hour, 1, [255, 0, 0])
        self.draw_digit(minute, 4, [0, 255, 0])
        self.draw_digit(second, 7, [0, 0, 255])
