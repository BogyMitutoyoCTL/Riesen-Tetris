from rainbow import *
import time

from field import Field
from painter import RGB_Field_Painter

if __name__ == "__main__":
    rgb_field_painter = RGB_Field_Painter()
    field_leds = Field(10, 20)
    for m in range(5, 50):
        for a in range(1, 50):
            for i in range(200):
                field_leds.set_pixel(i%10, i//10, hsv2rgb(i / 200 * m / 50 + a / 50, 1, 1))

            rgb_field_painter.draw(field_leds)

            time.sleep(0.05)