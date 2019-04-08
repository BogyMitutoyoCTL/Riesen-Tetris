from luma.core.render import canvas
from luma.led_matrix.device import ws2812

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
            # draw.ellipse((3, 5), fill=None, outline="green", width=2)
        time.sleep(100)

    def draw(self, field_to_print: Field):
        with canvas(self.device) as draw:
            for j in range(0, field_to_print.width):
                for i in range(0, field_to_print.height):
                    draw.point((i, j),
                               fill=(field_to_print.field[i][j][0], field_to_print.field[i][j][1],
                                     field_to_print.field[i][j][2]))


tetrisfield = Field(10, 20)

painter = RGB_Field_Painter()
painter.draw(tetrisfield)

while True:
    tetrisfield.set_block()
    painter.draw(tetrisfield)

    input()
    tetrisfield.generate_field()
