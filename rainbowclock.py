from time import sleep

from clock import Clock
from field import Field
from multiply import multiply
from rainbow import rainbowcolors


class Rainbowclock(Clock):
    def tick(self):

        self.led_matrix_painter.show_Text(self.get_date_string())
        back = Field(10, 20)

        COLORS = 60
        r = rainbowcolors(COLORS+20, (COLORS+20)/COLORS)
        currentrainbowstart = 0
        while True:
            currentrainbowstart += 1
            currentrainbowstart %= COLORS
            for x in range(10):
                for y in range(20):
                    back.set_pixel(x, y, r[y + currentrainbowstart])
            self.draw_clock()
            rainbowtime = multiply(back, self.field_leds)
            self.rgb_field_painter.draw(rainbowtime)
            sleep(0.05)

