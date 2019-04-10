import colorsys
from painter import RGB_Field_Painter
from field import Field
import time


def hsv2rgb(h, s, v):
    return tuple(round(i*255)for i in colorsys.hsv_to_rgb(h, s, v))


field_leds = Field(10, 20)
rgb_field_painter = RGB_Field_Painter()

for m in range(5, 50):
    for a in range(1, 50):
        for i in range(200):
            x = i%10
            y = i//10
            field_leds.set_pixel(x, y, hsv2rgb(i/200*m/50+a/50, 1, 1))

        rgb_field_painter.draw(field_leds)
        time.sleep(0.05)

