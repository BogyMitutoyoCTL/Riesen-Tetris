from random import random

from luma.core.render import canvas
from luma.led_matrix.device import ws2812
from luma.led_matrix.device import max7219
from luma.core import legacy
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.legacy.font import proportional, LCD_FONT

from block import Block, blocks, block_colors
from field import Field


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
        self.device.contrast(150)

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
                    r = field_to_print.field[i][j][0]
                    g = field_to_print.field[i][j][1]
                    b = field_to_print.field[i][j][2]
                    draw.point((i, j), fill=(r, g, b))


class Led_Matrix_Painter:
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, rotate=2, width=8, height=8, cascaded=4, block_orientation=-90)

        self.virtual = viewport(self.device, width=1000, height=8)

        self.amount_of_steps_for_message = 0
        self.position_of_Message_x = 0

    def show_Text(self, text: str):
        with canvas(self.virtual) as draw:
            legacy.text(draw, (0, 0), text, fill="white", font=proportional(LCD_FONT))

    def show_Message(self, message: str, amount_of_stepps_for_message: int):
        self.amount_of_steps_for_message = amount_of_stepps_for_message
        self.position_of_Message_x = 0
        self.virtual.set_position((0, 0))
        with canvas(self.virtual) as draw:
            # draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            draw.text((0, -2), "      "+message, fill="white")

    def move_Message(self):
        self.position_of_Message_x += 1
        if self.position_of_Message_x > self.amount_of_steps_for_message:
            self.position_of_Message_x = 0
        self.virtual.set_position((self.position_of_Message_x, 0))

    def draw(self, field_to_print: Field):
        self.virtual.set_position((0, 0))
        with canvas(self.virtual) as draw:
            for i in range(len(field_to_print.field)):
                for j in range(len(field_to_print.field[0])):
                    if field_to_print.field[i][j][0] + field_to_print.field[i][j][1] + field_to_print.field[i][j][2] > 0:
                        draw.point((j, i), fill="white")
                    else:
                        draw.point((j, i), fill="black")


if __name__ == "__main__":
    playfield = Field(10, 20)
    scoreboard = Field(32, 8)

    playfield_painter = RGB_Field_Painter()
    led_matrix_painter = Led_Matrix_Painter()

    while True:
        playfield.set_all_pixels_to_black()
        scoreboard.set_all_pixels_to_black()
        random_block_number = int(random() * 7)
        block = Block(blocks[random_block_number], block_colors[random_block_number])
        playfield.set_block(block, 3, 0)
        playfield_painter.draw(playfield)

        scoreboard.set_block(block.double_size(), 24, 1)
        led_matrix_painter.draw(scoreboard)

        input()
