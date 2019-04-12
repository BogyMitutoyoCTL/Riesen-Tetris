from time import sleep

from clock import Clock
from field import Field
from multiply import multiply
from painter import Led_Matrix_Painter, RGB_Field_Painter
from rainbow import rainbowcolors


class Rainbowclock(Clock):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Rainbowclock, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
        self.COLORS = 60
        self.r = rainbowcolors(self.COLORS + 20, (self.COLORS + 20) / self.COLORS)
        self.currentrainbowstart = 0


    def tick(self):
        self.led_matrix_painter.show_Text(self.get_date_string())
        back = Field(10, 20)

        self.currentrainbowstart += 1
        self.currentrainbowstart %= self.COLORS
        for x in range(10):
            for y in range(20):
                back.set_pixel(x, y, self.r[y + self.currentrainbowstart])
        self.draw_clock([255, 255, 255])
        rainbowtime = multiply(back, self.field_leds)
        self.rgb_field_painter.draw(rainbowtime)
        sleep(0.05)

