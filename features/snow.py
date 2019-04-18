import time
from random import random

from features.feature import Feature
from field import Field
from painter import Led_Matrix_Painter, RGB_Field_Painter


class Snow(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Snow, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)


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
            if color is None:
                self.field_leds.field[0][int(random() * self.field_leds.width)] = [int(random() * 255),
                                                                                   int(random() * 255),
                                                                                   int(random() * 255)]
            else:
                self.field_leds.field[0][int(random() * self.field_leds.width)] = color

    def tick(self):
        self.colored_snow([255, 255, 255])
        self.led_matrix_painter.show_Text("Snow")
        self.colored_snow()
        self.rgb_field_painter.draw(self.field_leds)
        time.sleep(0.1)

    def stop(self):
        pass
