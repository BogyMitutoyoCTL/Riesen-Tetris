import time
from random import random

from block import Block, blocks, block_colors
from feature import Feature
from field import Field
from highscorelist import Highscorelist
from painter import Led_Matrix_Painter, RGB_Field_Painter


class Startscreen(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Startscreen, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

    def draw_field_20(self):
        self.field_leds.set_all_pixels_to_black()
        for i in range(20):
            x = int(random() * self.field_leds.width)
            y = int(random() * self.field_leds.height)

            self.field_leds.field[y][x] = [int(random() * 255), int(random() * 255), int(random() * 255)]

    def change_some_pixel(self):
        for i in range(2):
            done = False
            while not done:
                x = int(random() * self.field_leds.width)
                y = int(random() * self.field_leds.height)

                self.field_leds.field[y][x] = [int(random() * 255), int(random() * 255), int(random() * 255)]

    def colored_snow(self, color: list=None):
        self.field_leds.delete_lines([self.field_leds.height-1])
        for i in range(int(random() * 3)):
            if color == None:
                self.field_leds.field[0][int(random() * self.field_leds.width)] = [int(random() * 255),
                                                                                   int(random() * 255),
                                                                                   int(random() * 255)]
            else:
                self.field_leds.field[0][int(random() * self.field_leds.width)] = color

    def new_block(self):
        zufall = int(random() * 7)

        self.block_today = Block(blocks[zufall], block_colors[zufall]).double_size()
        self.rotation_today = int(random()*4)

        # Block drehen
        for i in range(0, self.rotation_today):
            self.block_today.rotateleft()

        self.position_block_today_x = 1
        self.position_block_today_y = -8

    def falling_blocks(self):
        self.field_leds.set_all_pixels_to_black()
        self.field_leds.set_block(self.block_today, self.position_block_today_x, self.position_block_today_y)
        self.position_block_today_y += 1
        if self.position_block_today_y >= self.field_leds.height:
            self.new_block()

    def tick(self):
        # self.colored_snow([255, 255, 255])
        self.falling_blocks()
        self.rgb_field_painter.draw(self.field_leds)
        time.sleep(0.1)


if __name__ == "__main__":
    field_leds = Field(10, 20)
    field_matrix = Field(32, 8)
    rgb_field_painter = RGB_Field_Painter()
    led_matrix_painter = Led_Matrix_Painter()

    startscreen = Startscreen(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
    startscreen.new_block()

    while True:
        startscreen.tick()
