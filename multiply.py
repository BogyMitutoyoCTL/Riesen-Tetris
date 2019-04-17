from time import sleep

from clock import Clock
from field import Field
import numpy

from painter import RGB_Field_Painter, Led_Matrix_Painter
from rainbow import rainbowcolors


def multiply(background: Field, foreground: Field):
    white = Field(10,20)
    for x in range(10):
        for y in range(20):
            white.set_pixel(x, y, [255, 255, 255])

    bg = numpy.array(background.field)
    fg = numpy.array(foreground.field)
    multi = numpy.multiply(bg, fg)
    multi = numpy.divide(multi, white.field)
    combined = Field(10, 20)
    combined.field = multi.astype(int).tolist()
    return combined


if __name__ == "__main__":
    back = Field(10, 20)

    fore = Field(10, 20)
    rainbowclock = Field(10, 20)
    rgb_field_painter = RGB_Field_Painter()
    clock = Clock(fore, Field(32, 8), rgb_field_painter, Led_Matrix_Painter())
    COLORS = 60
    r = rainbowcolors(COLORS)
    currentrainbowstart = 0
    while True:
        currentrainbowstart +=1
        currentrainbowstart %= COLORS-20
        for x in range(10):
            for y in range(20):
                back.set_pixel(x, y, r[y+currentrainbowstart])
        clock.draw_clock([255, 255, 255])
        rainbowtime = multiply(back, fore)
        rgb_field_painter.draw(rainbowtime)
        sleep(0.05)
