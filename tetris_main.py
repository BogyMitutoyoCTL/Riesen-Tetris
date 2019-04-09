import time
import _thread
from random import random

from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter, Console_Painter
from block import Block, blocks


class Tetris_Main:
    def __init__(self):
        # Felder erstellen
        self.field_leds = Field(10, 20)
        self.field_matrix = Field(32, 8)

        # Painter erstellen
        self.rgb_field_painter = RGB_Field_Painter()
        self.led_matrix_painter = Led_Matrix_Painter()

        # block erstellen
        self.block_today = Block(blocks[0])
        self.block_future = Block(blocks[0])

        # Blockeigenschaften
        self.random_number_today = int(random()*6)
        self.random_number_future = int(random()*6)
        self.rotation_today = int(random() * 4)
        self.rotation_future = int(random() * 4)

        # Positionen block_today
        self.position_block_today_x = 3
        self.position_block_today_y = 0

    def new_block(self):
        self.random_number_today = self.random_number_future
        self.random_number_future = int(random()*6)

        self.rotation_today = self.rotation_future
        self.rotation_future = int(random() * 4)

        # todo: ändere die Parameter, damit die Blöcke wirklich am Rand erscheinen
        self.position_block_today_x = 3
        self.position_block_today_y = 0

    def refresh_painter(self):
        # Blöcke aussuchen
        self.block_today = Block(blocks[self.random_number_today])
        self.block_future = Block(blocks[self.random_number_future])

        # Blöcke drehen
        for i in range(0, self.rotation_today):
            self.block_today.rotateleft()
        for i in range(self.rotation_future):
            self.block_future.rotateleft()

        # Blöcke auf das LED Feld malen
        self.field_leds.set_block(self.block_today, self.position_block_today_x, self.position_block_today_y)
        self.rgb_field_painter.draw(self.field_leds)

        # Blöcke auf die Matrix schreiben
        self.field_matrix.set_all_pixels_to_black()
        self.field_matrix.set_block(self.block_future.double_size(), 24, 0)
        self.led_matrix_painter.draw(self.field_matrix)

    def delete_block_today(self):
        self.field_leds.remove_block(self.block_today, self.position_block_today_x, self.position_block_today_y)

    def set_all_fields_black(self):
        self.field_leds.set_all_pixels_to_black()
        self.field_matrix.set_all_pixels_to_black()

    def move_block_today_one_step_down(self):
        self.position_block_today_y += 1


def console_listener():
    while True:
        tetris_main.refresh_painter()

        time.sleep(1)

        tetris_main.delete_block_today()
        tetris_main.move_block_today_one_step_down()


tetris_main = Tetris_Main()
tetris_main.set_all_fields_black()

_thread.start_new_thread(console_listener(), ())

while True:
    input()
    tetris_main.new_block()
    tetris_main.refresh_painter()
