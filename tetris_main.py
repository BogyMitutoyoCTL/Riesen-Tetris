import time
import threading
import pygame
from pygame.locals import *
from random import random

from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter, Console_Painter
from block import Block, blocks, block_colors

lock = threading.Lock()


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
        self.rotation_today = int(random() * 4)
        self.rotation_future = int(random() * 4)

        self.refresh_blocks()

        # Positionen block_today
        self.position_block_today_x = 3
        self.position_block_today_y = -self.block_today.get_line_of_first_pixel() - 2

        pygame.init()
        screen = pygame.display.set_mode((200, 200))

    def new_block(self):
        self.check_for_full_lines()

        self.random_number_today = self.random_number_future
        self.random_number_future = int(random() * 6)

        self.rotation_today = self.rotation_future
        self.rotation_future = int(random() * 4)

        self.refresh_blocks()

        self.position_block_today_x = 3
        self.position_block_today_y = -self.block_today.get_line_of_first_pixel() - 1

    def check_for_full_lines(self):
        print("Test for full lines")
        self.field_leds.test_for_full_lines()

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
            print("Kollision erkannt -> neuer Block")
            self.refresh_painter()
            self.new_block()
            self.move_block_today_one_step_down()
            self.refresh_painter()
        else:
            self.position_block_today_y += 1
            self.refresh_blocks()
            self.refresh_painter()

    def move_block_today_one_step_left(self):
        self.delete_block_today()

        if self.field_leds.test_for_collision(
                self.block_today,
                self.position_block_today_x - 1,
                self.position_block_today_y):
            print("Kollision erkannt -> keine Bewegung nach links")
        else:
            self.position_block_today_x -= 1
            self.refresh_blocks()
            self.refresh_painter()

    def move_block_today_one_step_right(self):
        self.delete_block_today()

        if self.field_leds.test_for_collision(
                self.block_today,
                self.position_block_today_x + 1,
                self.position_block_today_y):
            print("Kollision erkannt -> keine Bewegung nach rechts")
        else:
            self.position_block_today_x += 1
            self.refresh_blocks()
            self.refresh_painter()

    def rotate_block_today_left(self):
        self.delete_block_today()
        block_today_for_test = Block(self.block_today.get_rotated_left(), 0)

        if self.field_leds.test_for_collision(
                block_today_for_test,
                self.position_block_today_x,
                self.position_block_today_y):
            print("Kollision erkannt -> keine Rotation nach links")
        else:
            self.rotation_today += 1
            if self.rotation_today >= 4:
                self.rotation_today -= 4
            self.refresh_blocks()
            self.refresh_painter()

    def rotate_block_today_right(self):
        self.delete_block_today()
        block_today_for_test = Block(self.block_today.get_rotated_right(), 0)

        if self.field_leds.test_for_collision(
                block_today_for_test,
                self.position_block_today_x,
                self.position_block_today_y):
            print("Kollision erkannt -> keine Rotation nach rechts")
        else:
            self.rotation_today -= 1
            if self.rotation_today < 0:
                self.rotation_today += 4
            self.refresh_blocks()
            self.refresh_painter()

    def tick(self):
        self.move_block_today_one_step_down()
        self.refresh_painter()

    def control(self):
        while True:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            lock.acquire()
            if keys[K_n]:  # neuer Block
                print("Taste gedrückt")
                self.new_block()
                self.refresh_painter()
                self.control_wait_for_release(K_n)
            elif keys[K_q]:  # rotate left
                print("Taste gedrückt")
                self.rotate_block_today_left()
                self.control_wait_for_release(K_q)
            elif keys[K_e]:  # rotate right
                print("Taste gedrückt")
                self.rotate_block_today_right()
                self.control_wait_for_release(K_e)
            elif keys[K_a]:  # move left
                print("Taste gedrückt")
                self.move_block_today_one_step_left()
                self.control_wait_for_release(K_a)
            elif keys[K_d]:  # move right
                print("Taste gedrückt")
                self.move_block_today_one_step_right()
                self.control_wait_for_release(K_d)
            elif keys[K_s]:  # move down
                print("Taste gedrückt")
                self.tick()
                self.control_wait_for_release(K_s)
            lock.release()

    def control_wait_for_release(self, key):
        lock.release()
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        while keys[key]:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
        print("Taste losgelassen")
        lock.acquire()


tetris_main = Tetris_Main()
tetris_main.set_all_fields_black()

# tetris_main.field_leds.set_pixel(0, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(1, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(2, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(3, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(4, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(6, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(7, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(8, 19, [255, 255, 0])
# tetris_main.field_leds.set_pixel(9, 19, [255, 255, 0])

thread_for_control = threading.Thread(target=tetris_main.control)       # ohne () nach target=tetris_main.control
thread_for_control.daemon = True
thread_for_control.start()

count = 0
while True:
    lock.acquire()
    tetris_main.tick()
    lock.release()
    time.sleep(0.5)
