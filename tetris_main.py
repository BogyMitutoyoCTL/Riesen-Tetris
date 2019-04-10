import time
import _thread
import threading
import pygame
from pygame.constants import K_ESCAPE
from pygame.locals import *
from random import random

from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter, Console_Painter
from block import Block, blocks, block_colors


class Tetris_Main:
    def __init__(self):
        # Felder erstellen
        self.field_leds = Field(10, 20)
        self.field_matrix = Field(32, 8)

        # Painter erstellen
        self.rgb_field_painter = RGB_Field_Painter()
        self.led_matrix_painter = Led_Matrix_Painter()

        # block erstellen
        self.block_today = Block(blocks[0], block_colors[0])
        self.block_future = Block(blocks[0], block_colors[0])

        # Blockeigenschaften
        self.random_number_today = int(random() * 6)
        self.random_number_future = int(random() * 6)
        # self.rotation_today = int(random() * 4)
        self.rotation_today = 0
        self.rotation_future = 0

        # Positionen block_today
        self.position_block_today_x = 3
        self.position_block_today_y = 0

        self.refresh_blocks()

    def new_block(self):
        self.random_number_today = self.random_number_future
        self.random_number_future = int(random() * 6)

        self.rotation_today = self.rotation_future
        self.rotation_future = 0

        # todo: ändere die Parameter, damit die Blöcke wirklich am Rand erscheinen
        self.position_block_today_x = 3
        self.position_block_today_y = 0

    def refresh_blocks(self):
        # Blöcke aussuchen
        self.block_today = Block(blocks[self.random_number_today], block_colors[self.random_number_today])
        self.block_future = Block(blocks[self.random_number_future], block_colors[self.random_number_future])

        # Blöcke drehen
        for i in range(0, self.rotation_today):
            self.block_today.rotateleft()
        for i in range(self.rotation_future):
            self.block_future.rotateleft()

    def refresh_painter(self):
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

        self.delete_block_today()

        if self.field_leds.test_for_collision(
                self.block_today,
                self.position_block_today_x,
                self.position_block_today_y + 1):
            self.refresh_painter()
            self.new_block()
            self.refresh_blocks()
            self.refresh_painter()
            print("Kollision erkannt -> neuer Block")
        else:
            self.position_block_today_y += 1
            self.refresh_blocks()
            self.refresh_painter()

    def tick(self):
        self.move_block_today_one_step_down()
        self.refresh_painter()
        time.sleep(0.3)

    def control(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_n]:   # neuer Block
            print("Taste gedrückt")
            self.new_block()
            self.refresh_blocks()
            self.refresh_painter()
            self.control_wait_for_release(K_n)

    def control_wait_for_release(self, key):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        while keys[key]:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
        print("Taste losgelassen")


tetris_main = Tetris_Main()
tetris_main.set_all_fields_black()

# tetris_main.field_leds.set_pixel(5, 18, [255, 255, 0])


pygame.init()
screen = pygame.display.set_mode((200, 200))

number = 0
done = False
while True:
    tetris_main.tick()
    tetris_main.control()
