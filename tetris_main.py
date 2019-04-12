import random as random_music
import threading
import time
from random import random

import pygame

import game_sound
from block import Block, blocks, block_colors
from feature import Feature
from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter
from Score import *

lock = threading.Lock()
tetris_songs = ['./sound-files/lied.mp3', './sound-files/lied2.mp3']


class Tetris_Main(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Tetris_Main, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

        self.prepare_for_start()

        pygame.init()
        screen = pygame.display.set_mode((200, 200))

        game_sound.init_mixer()

    def __new_block(self):
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

        deletablelines = self.field_leds.get_all_full_lines()
        if len(deletablelines) > 0:
            game_sound.play_sound("breaking_line")
            time.sleep(0.2)
            self.field_leds.delete_lines(deletablelines)
            self.score.score_for_line(len(deletablelines))

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
        self.score.draw_score_on_field()
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
            game_sound.stop_song()
            game_sound.play_sound("game_over")
            self.led_matrix_painter.show_Message("Game over - Your Points: "+str(123456), 250)
        elif self.field_leds.give_type_of_collision(
                self.block_today,
                self.position_block_today_x,
                self.position_block_today_y + 1) == 1:
            print(" -> neuer Block")
            self.refresh_led_painter()
            self.__new_block()
            self.score.score_for_block()
            self.refresh_matrix_painter()
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
        if not self.game_over:
            self.move_block_today_one_step_down()
            game_sound.play_new_musik_if_music_is_over(tetris_songs)
        else:
            self.led_matrix_painter.move_Message()
            time.sleep(0.02)
        lock.release()

        if not self.game_over:
            self.get_delay()
            print(self.delay)
            time.sleep(self.delay)  # TODO: Delay anpassen

    def event(self, eventname: str):
        lock.acquire()
        if not self.game_over:
            if eventname == "new":  # neuer Block    # todo: später rauswerfen (Johannes)
                self.__new_block()
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

    def get_delay(self):
        if self.score.get_score_int() < 50:
            self.delay = 0.4
        elif self.score.get_score_int() < 100:
            self.delay = 0.3
        elif self.score.get_score_int() < 500:
            self.delay = 0.25
        elif self.score.get_score_int() < 1000:
            self.delay = 0.2
        elif self.score.get_score_int() < 2000:
            self.delay = 0.15
        elif self.score.get_score_int() < 5000:
            self.delay = 0.12
        elif self.score.get_score_int() < 10000:
            self.delay = 0.1
        elif self.score.get_score_int() < 20000:
            self.delay = 0.09
        elif self.score.get_score_int() < 50000:
            self.delay = 0.07
        elif self.score.get_score_int() < 100000:
            self.delay = 0.06
        else:
            self.delay = 0.05

    def start(self):
        self.prepare_for_start()

        self.refresh_led_painter()
        self.refresh_matrix_painter()

        self.game_over = False

        game_sound.play_random_song(tetris_songs)

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

        self.score = Score(self.field_matrix)

    def stop(self) -> None:
        self.game_over = True
        game_sound.stop_song()

    def is_game_over(self) -> bool:
        return self.game_over
