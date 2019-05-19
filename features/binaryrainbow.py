from features.binaryclock import BinaryClock
from field import Field
from multiply import multiply
from painter import Led_Matrix_Painter, RGB_Field_Painter
from rainbow import rainbowcolors


class BinaryRainbow(BinaryClock):

    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(BinaryRainbow, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
        self.COLORS = 60
        self.r = rainbowcolors(self.COLORS + 20, (self.COLORS + 20) / self.COLORS)
        self.currentrainbowstart = 0

    def draw_clock(self, color: list = None):
        hour, minute, second = self.get_time()
        self.draw_digit(hour, 1, [255, 255, 255])
        self.draw_digit(minute, 4, [255, 255, 255])
        self.draw_digit(second, 7, [255, 255, 255])
        back = Field(10, 20)

        self.currentrainbowstart += 1
        self.currentrainbowstart %= self.COLORS
        for x in range(10):
            for y in range(20):
                back.set_pixel(x, y, self.r[y + self.currentrainbowstart])
        rainbowtime = multiply(back, self.field_leds)
        self.field_leds.field = rainbowtime.field
