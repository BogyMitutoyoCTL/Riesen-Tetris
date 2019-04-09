from luma.core.render import canvas
from luma.led_matrix.device import ws2812
from luma.led_matrix.device import max7219
from luma.core import legacy
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.legacy.font import proportional, LCD_FONT

from field import Field
import time


class Console_Painter:
    def draw(self, field_to_print: Field):
        print("Feldbreite: " + str(field_to_print.width) + "; Höhe: " + str(field_to_print.height))
        text = ""
        for j in range(0, field_to_print.height):
            for i in range(0, field_to_print.width):
                if (field_to_print.field[j][i][0] + field_to_print.field[j][i][1] + field_to_print.field[j][i][2]) > 0:
                    text += "x"
                else:
                    text += "_"
            text += "\n"
        print(text)
        print("--------------------------")


class RGB_Field_Painter:
    def __init__(self):
        self.device = ws2812(width=10, height=20, rotate=1)
        self.device.contrast(255)

    def draw_a_test(self):
        with canvas(self.device) as draw:
            draw.rectangle((0, 0, 19, 9), fill=None, outline="white")
            draw.point((0, 0), fill="yellow")
            draw.point((4, 0), fill="blue")
            draw.point((11, 0), fill="orange")
            draw.point((4, 4), fill=(255, 0, 0))
            draw.point((19, 0), fill=(0, 255, 0))

    def draw(self, field_to_print: Field):
        with canvas(self.device) as draw:
            for j in range(0, field_to_print.width):
                for i in range(0, field_to_print.height):
                    draw.point((i, j),
                               fill=(field_to_print.field[i][j][0], field_to_print.field[i][j][1],
                                     field_to_print.field[i][j][2]))


class Led_Matrix:
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, rotate=2, width=8, height=8, cascaded=4, block_orientation=-90)

        self.virtual = viewport(self.device, width=500, height=8)

    def show_Text(self, text: str):
        with canvas(self.virtual) as draw:
            legacy.text(draw, (0, 0), text, fill="white", font=proportional(LCD_FONT))

    def show_matrix(self, field_to_print: Field):
        with canvas(self.virtual) as draw:
            for i in range(len(field_to_print.field)):
                for j in range(len(field_to_print.field[0])):
                    if field_to_print.field[i][j][0]+field_to_print.field[i][j][1]+field_to_print.field[i][j][2] > 0:
                        draw.point((i, j), fill="white")
                    else:
                        draw.point((i, j), fill="black")


field_tetris = Field(10, 20)

painter = RGB_Field_Painter()
painter.draw(field_tetris)

field_matrix = Field(32, 8)
led_matrix = Led_Matrix()
led_matrix.show_Text(text="12345")

while True:
    field_tetris.set_block()
    painter.draw(field_tetris)

    input()
    field_tetris.set_all_pixels_to_black()
    led_matrix.show_matrix(field_matrix)
