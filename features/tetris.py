import threading
from copy import deepcopy
import pygame
import game_sound
from block import TetrisBlock
from features.feature import Feature
from painter import RGB_Field_Painter
from highscorelist import *

lock = threading.Lock()
tetris_songs = ['./sound-files/lied.mp3', './sound-files/lied2.mp3']


class Tetris(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter, highscorelist: Highscorelist):
        super(Tetris, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter,
                                     highscorelist)
        self.next_block = TetrisBlock.get_random_block()
        self.current_block = TetrisBlock.get_random_block()
        self.score = Score()
        self.prepare_for_start()
        pygame.init()
        game_sound.init_mixer()

    def __new_block(self):
        self.check_for_full_lines()

        self.current_block = self.next_block
        self.next_block = TetrisBlock.get_random_block()

        self.position_block_today_x = 3
        self.position_block_today_y = -self.current_block.get_line_of_first_pixel_from_bottom() - 1  # evtl. mit -1 am Ende

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

    def refresh_led_painter(self):
        # Blöcke auf das LED Feld malen
        self.field_leds.set_block(self.current_block, self.position_block_today_x, self.position_block_today_y)
        self.rgb_field_painter.draw(self.field_leds)

    def refresh_matrix_painter(self):
        # Blöcke auf die Matrix schreiben
        self.field_matrix.set_all_pixels_to_black()
        self.score.draw_score_on_field(self.field_matrix)
        self.field_matrix.set_block(self.next_block.double_size(), 24, 0)
        self.led_matrix_painter.draw(self.field_matrix)

    def delete_current_block(self):
        self.field_leds.remove_block(self.current_block, self.position_block_today_x, self.position_block_today_y)

    def set_all_fields_black(self):
        self.field_leds.set_all_pixels_to_black()
        self.field_matrix.set_all_pixels_to_black()

    def move_block_today_one_step_down(self):
        self.delete_current_block()

        collision = self.field_leds.give_type_of_collision(self.current_block, self.position_block_today_x,
                                                           self.position_block_today_y + 1)

        if collision == Field.GameOverCollision:
            print(" -> Game over")
            self.game_over = True
            game_sound.stop_song()
            game_sound.play_sound("game_over")
            self.highscorelist.add_entry(
                Highscoreentry(datetime.today(), self.playername, self.score.get_score_int()))
            self.highscorelist.save()
            self.led_matrix_painter.show_Message("Game over - Your Points: " + self.score.get_score_str(), 250)
        elif collision == Field.Collision:
            game_sound.play_sound("tick")
            print(" -> neuer Block")
            self.refresh_led_painter()
            self.__new_block()
            self.score.score_for_block()
            self.refresh_matrix_painter()
        else:
            self.position_block_today_y += 1
            self.refresh_led_painter()

    def move_block_today_one_step_left(self):
        self.delete_current_block()

        if self.field_leds.give_type_of_collision(
                self.current_block,
                self.position_block_today_x - 1,
                self.position_block_today_y) != Field.NoCollision:
            print(" -> keine Bewegung nach links")
        else:
            self.position_block_today_x -= 1
            self.refresh_led_painter()

    def move_block_today_one_step_right(self):
        self.delete_current_block()

        if self.field_leds.give_type_of_collision(
                self.current_block,
                self.position_block_today_x + 1,
                self.position_block_today_y) != Field.NoCollision:
            print(" -> keine Bewegung nach rechts")
        else:
            self.position_block_today_x += 1
            self.refresh_led_painter()

    def rotate_block_today_left(self):
        self.delete_current_block()
        block_today_for_test = self.current_block.clone()
        block_today_for_test.rotateleft()

        if self.field_leds.give_type_of_collision(
                block_today_for_test,
                self.position_block_today_x,
                self.position_block_today_y) != Field.NoCollision:
            print(" -> keine Rotation nach links")
        else:
            self.current_block.rotateleft()
            self.refresh_led_painter()

    def rotate_block_today_right(self):
        self.delete_current_block()
        block_today_for_test = self.current_block.clone()
        block_today_for_test.rotateright()

        if self.field_leds.give_type_of_collision(
                block_today_for_test,
                self.position_block_today_x,
                self.position_block_today_y) != Field.NoCollision:
            print(" -> keine Rotation nach rechts")
        else:
            self.current_block.rotateright()
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
            time.sleep(self.get_delay())

    def event(self, eventname: str):
        lock.acquire()
        if not self.game_over:
            if eventname == "new":  # neuer Block    # todo: später rauswerfen (Johannes)
                self.__new_block()
            elif eventname == "rotate left":
                self.rotate_block_today_left()
            elif eventname == "rotate right":
                self.rotate_block_today_right()
            elif eventname == "move left":
                self.move_block_today_one_step_left()
            elif eventname == "move right":
                self.move_block_today_one_step_right()
            elif eventname == "move down":
                self.move_block_today_one_step_down()
        lock.release()

    def get_delay(self):
        speedmap = [(50, 0.4), (100, 0.35), (500, 0.3), (1000, 0.25), (2000, 0.2), (5000, 0.15), (10000, 0.12), (20000, 0.09),
                     (50000, 0.07), (100000, 0.06)]
        for score, delay in speedmap:
            if self.score.points < score:
                return delay
        return 0.05

    def start(self, playername: str = None):
        super(Tetris, self).start(playername)
        self.prepare_for_start()
        self.refresh_led_painter()
        self.refresh_matrix_painter()
        self.game_over = False
        game_sound.play_random_song(tetris_songs)

    def prepare_for_start(self):
        self.set_all_fields_black()

        # Positionen block_today
        self.position_block_today_x = 3
        self.position_block_today_y = -self.current_block.get_line_of_first_pixel_from_bottom() - 2

        # self.draw_lines_for_test()

    def stop(self) -> None:
        self.game_over = True
        game_sound.stop_song()

    def is_game_over(self):
        return super(Tetris, self).is_game_over()

    def draw_lines_for_test(self):
        for x in range(self.field_leds.width):
            self.field_leds.field[19][x] = [0, 255, 100]
            self.field_leds.field[18][x] = [0, 255, 100]
        self.field_leds.field[18][5] = [0, 0, 0]
        self.field_leds.field[19][5] = [0, 0, 0]
