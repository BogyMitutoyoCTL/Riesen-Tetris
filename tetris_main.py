import time
import threading
import pygame
import game_sound
from pygame.locals import *
from random import random
import random as random_music

from feature import Feature
from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter, Console_Painter
from block import Block, blocks, block_colors

lock = threading.Lock()
_songs = ['./sound-files/lied.mp3', './sound-files/lied2.mp3']


class Tetris_Main(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Tetris_Main, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

        self.prepare_for_start()

        pygame.init()
        screen = pygame.display.set_mode((200, 200))

        game_sound.init_mixer()

    def new_block(self):
        self.check_for_full_lines()

        self.random_number_today = self.random_number_future
        self.random_number_future = int(random() * 7)

        self.rotation_today = self.rotation_future
        self.rotation_future = int(random() * 4)

        self.refresh_blocks()

        self.position_block_today_x = 3
        self.position_block_today_y = -self.block_today.get_line_of_first_pixel_from_bottom() - 1  # evtl. mit -1 am Ende

        self.refresh_led_painter()
        self.refresh_matrix_painter()

    def check_for_full_lines(self):
        self.field_leds.delete_all_full_lines()

    def refresh_blocks(self):
        # Blöcke aussuchen
        self.block_today = Block(blocks[self.random_number_today], block_colors[self.random_number_today])
        self.block_future = Block(blocks[self.random_number_future], block_colors[self.random_number_future])

        # Blöcke drehen
        for i in range(0, self.rotation_today):
            self.block_today.rotateleft()
        for i in range(self.rotation_future):
            self.block_future.rotateleft()

    def refresh_led_painter(self):
        # Blöcke auf das LED Feld malen
        self.field_leds.set_block(self.block_today, self.position_block_today_x, self.position_block_today_y)
        self.rgb_field_painter.draw(self.field_leds)

    def refresh_matrix_painter(self):
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

        if self.field_leds.give_type_of_collision(
                self.block_today,
                self.position_block_today_x,
                self.position_block_today_y + 1) == 2:
            print(" -> Game over")
            self.game_over = True
        elif self.field_leds.give_type_of_collision(
                self.block_today,
                self.position_block_today_x,
                self.position_block_today_y + 1) == 1:
            print(" -> neuer Block")
            self.refresh_led_painter()
            self.new_block()
        else:
            self.position_block_today_y += 1
            self.refresh_led_painter()

    def move_block_today_one_step_left(self):
        self.delete_block_today()

        if self.field_leds.give_type_of_collision(
                self.block_today,
                self.position_block_today_x - 1,
                self.position_block_today_y) != 0:
            print(" -> keine Bewegung nach links")
        else:
            self.position_block_today_x -= 1
            self.refresh_led_painter()

    def move_block_today_one_step_right(self):
        self.delete_block_today()

        if self.field_leds.give_type_of_collision(
                self.block_today,
                self.position_block_today_x + 1,
                self.position_block_today_y) != 0:
            print(" -> keine Bewegung nach rechts")
        else:
            self.position_block_today_x += 1
            self.refresh_led_painter()

    def rotate_block_today_left(self):
        self.delete_block_today()
        block_today_for_test = Block(self.block_today.get_rotated_left(), 0)

        if self.field_leds.give_type_of_collision(
                block_today_for_test,
                self.position_block_today_x,
                self.position_block_today_y) != 0:
            print(" -> keine Rotation nach links")
        else:
            self.rotation_today += 1
            if self.rotation_today >= 4:
                self.rotation_today -= 4
            self.refresh_blocks()
            self.refresh_led_painter()

    def rotate_block_today_right(self):
        self.delete_block_today()
        block_today_for_test = Block(self.block_today.get_rotated_right(), 0)

        if self.field_leds.give_type_of_collision(
                block_today_for_test,
                self.position_block_today_x,
                self.position_block_today_y) != 0:
            print(" -> keine Rotation nach rechts")
        else:
            self.rotation_today -= 1
            if self.rotation_today < 0:
                self.rotation_today += 4
            self.refresh_blocks()
            self.refresh_led_painter()

    def tick(self):
        lock.acquire()
        self.move_block_today_one_step_down()

        for event in pygame.event.get():  # plays new music if music is over
            if event.type == pygame.QUIT:
                print("New Music")
                pygame.time.wait(250)
                next_song = random_music.choice(_songs)
                game_sound.play_song(next_song)
        lock.release()

        if self.delay > 0.15:
            self.delay -= 0.001
        time.sleep(self.delay) # TODO: Delay einbauen

    def event(self, eventname: str):
        lock.acquire()
        if eventname == "new":  # neuer Block    # todo: später rauswerfen (Johannes)
            self.new_block()
        elif eventname == "rotate left":  # rotate left
            self.rotate_block_today_left()
        elif eventname == "rotate right":  # rotate right
            self.rotate_block_today_right()
        elif eventname == "move left":  # move left
            self.move_block_today_one_step_left()
        elif eventname == "move right":  # move right
            self.move_block_today_one_step_right()
        elif eventname == "move down":  # move down
            self.move_block_today_one_step_down()
        lock.release()

    def start(self):
        self.prepare_for_start()

        self.refresh_led_painter()
        self.refresh_matrix_painter()

        self.game_over = False

        game_sound.play_song(random_music.choice(_songs))

    def prepare_for_start(self):
        self.set_all_fields_black()

        # Blockeigenschaften
        self.random_number_today = int(random() * 7)
        self.random_number_future = int(random() * 7)
        self.rotation_today = int(random() * 4)
        self.rotation_future = int(random() * 4)

        self.refresh_blocks()

        # Positionen block_today
        self.position_block_today_x = 3
        self.position_block_today_y = -self.block_today.get_line_of_first_pixel_from_bottom() - 2

        self.delay = 0.5

    def stop(self):
        self.game_over = True
        game_sound.stop_song()

    def is_game_over(self) -> bool:
        return self.game_over
