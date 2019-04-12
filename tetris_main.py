import threading
from random import random
from copy import deepcopy

import pygame

import game_sound
from block import Block, blocks, block_colors
from feature import Feature
from painter import RGB_Field_Painter
from highscorelist import *

lock = threading.Lock()
tetris_songs = ['./sound-files/lied.mp3', './sound-files/lied2.mp3']


class Tetris_Main(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter, highscorelist: Highscorelist):
        super(Tetris_Main, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter,
                                          highscorelist)
        self.prepare_for_start()
        pygame.init()
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
            self.blink_deleted_lines(deletablelines)
            self.field_leds.delete_lines(deletablelines)
            self.score.score_for_line(len(deletablelines))

    def blink_deleted_lines(self, deletablelines: list):
        colors_in_line = deepcopy(self.field_leds.field)
        colors_for_blink = [1, 0, 1, 0]

        for color in colors_for_blink:
            for y in deletablelines:
                for x in range(self.field_leds.width):
                    if color == 1:
                        self.field_leds.field[y][x] = [255, 255, 255]
                    else:
                        self.field_leds.field[y][x] = colors_in_line[y][x]

            self.rgb_field_painter.draw(self.field_leds)
            time.sleep(0.03)

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
        self.score.draw_score_on_field(self.field_matrix)
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
            self.highscorelist.add_entry(
                Highscoreentry(datetime.today(), self.playername, self.score.get_score_int()))
            self.highscorelist.save()
            self.led_matrix_painter.show_Message("Game over - Your Points: " + str(self.score.get_score_str()), 250)
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
            if self.delay > 0.15:
                self.delay -= 0.001
            time.sleep(self.delay)  # TODO: Delay einbauen

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

    def start(self, playername: str=None):
        super(Tetris_Main, self).start(playername)
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

        self.delay = 0.5

        self.score = Score()

        # self.draw_lines_for_test()

    def stop(self) -> None:
        self.game_over = True
        game_sound.stop_song()

    def is_game_over(self) -> bool:
        return self.game_over

    def draw_lines_for_test(self):
        for x in range(self.field_leds.width):
            self.field_leds.field[19][x] = [0, 255, 100]
            self.field_leds.field[18][x] = [0, 255, 100]
        self.field_leds.field[18][5] = [0, 0, 0]
        self.field_leds.field[19][5] = [0, 0, 0]
