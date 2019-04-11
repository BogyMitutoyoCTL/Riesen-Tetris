from clock import Clock
from field import Field
import numpy

from painter import RGB_Field_Painter, Led_Matrix_Painter


def multiply(background: Field, foreground: Field):
    bg = numpy.array(background.field)
    fg = numpy.array(foreground.field)
    multi = numpy.multiply(bg, fg)
    combined = Field(10,20)
    combined.field = multi.tolist()
    return combined


if __name__ == "__main__":
    back = Field(10, 20)
    fore = Field(10, 20)
    rainbowclock = Field(10, 20)
    rgb_field_painter = RGB_Field_Painter()
    clock = Clock(fore, Field(32, 8), rgb_field_painter, Led_Matrix_Painter())
    while True:
        clock.draw_clock()
        rainbowtime = multiply(back, fore)
        rgb_field_painter.draw(rainbowtime)
