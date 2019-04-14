import time
from copy import deepcopy
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

        self.blocknumber_last_time = -1

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

    def colored_snow(self, color: list = None):
        self.field_leds.delete_lines([self.field_leds.height - 1])
        for i in range(int(random() * 3)):
            if color == None:
                self.field_leds.field[0][int(random() * self.field_leds.width)] = [int(random() * 255),
                                                                                   int(random() * 255),
                                                                                   int(random() * 255)]
            else:
                self.field_leds.field[0][int(random() * self.field_leds.width)] = color

    def new_block(self):
        zufall = self.blocknumber_last_time
        while self.blocknumber_last_time == zufall:
            zufall = int(random() * 7)
        self.blocknumber_last_time = zufall
        self.block_top = Block(blocks[zufall], block_colors[zufall]).double_size()
        self.rotation_block_top = int(random() * 4)

        # Block drehen
        for i in range(0, self.rotation_block_top):
            self.block_top.rotateleft()

        self.position_block_top_x = int(
            random() * (self.field_leds.width
                        - self.block_top.get_line_of_first_pixel_from_right()
                        + self.block_top.get_line_of_first_pixel_from_left())) \
                                    - self.block_top.get_line_of_first_pixel_from_left()
        self.position_block_top_y = -self.block_top.get_line_of_first_pixel_from_bottom()

    def falling_blocks(self):
        self.field_leds.set_all_pixels_to_black()
        self.position_block_bottom_y += 1
        if self.position_block_bottom_y >= self.field_leds.height:
            self.copy_block_top_to_block_bottom()
            self.new_block()
        self.field_leds.set_block(self.block_bottom, self.position_block_bottom_x, self.position_block_bottom_y)

        if self.position_block_bottom_y + self.block_bottom.get_line_of_first_pixel_from_top() >= self.field_leds.height/4*3:
            self.field_leds.set_block(self.block_top, self.position_block_top_x, self.position_block_top_y)
            self.position_block_top_y += 1

    def tick(self):
        if self.mode == "snow":
            self.colored_snow([255, 255, 255])
            time.sleep(0.2)
        elif self.mode == "falling_blocks":
            self.falling_blocks()
            time.sleep(0.02)
        self.rgb_field_painter.draw(self.field_leds)

    def copy_block_top_to_block_bottom(self):
        self.block_bottom = deepcopy(self.block_top)
        self.position_block_bottom_x = deepcopy(self.position_block_top_x)
        self.position_block_bottom_y = deepcopy(self.position_block_top_y)
        self.rotation_block_bottom = deepcopy(self.rotation_block_top)

    def start(self, playername: str = None, mode: str = "snow"):
        super(Startscreen, self).start(playername)
        self.mode = mode
        if self.mode == "falling_blocks":
            self.new_block()
            self.copy_block_top_to_block_bottom()

    def stop(self):
        pass


if __name__ == "__main__":
    field_leds = Field(10, 20)
    field_matrix = Field(32, 8)
    rgb_field_painter = RGB_Field_Painter()
    led_matrix_painter = Led_Matrix_Painter()

    startscreen = Startscreen(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
    startscreen.start(mode="snow")

    while True:
        startscreen.tick()
