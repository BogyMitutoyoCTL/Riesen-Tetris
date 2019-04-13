import time
from random import random

import game_sound
from Score import Score
from feature import Feature
from field import Field
from highscorelist import Highscorelist
from painter import RGB_Field_Painter, Led_Matrix_Painter

BLACK = [0, 0, 0]


class Snake_Main(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter, highscorelist: Highscorelist = Highscorelist("Not_used")):
        super(Snake_Main, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter, highscorelist)

    def event(self, eventname: str):
        if not self.is_there_a_direction_change_in_this_tick:
            if eventname == "move up":
                if self.direction != 2:
                    self.direction = 0
                    self.is_there_a_direction_change_in_this_tick = True
            elif eventname == "move left":
                if self.direction != 3:
                    self.direction = 1
                    self.is_there_a_direction_change_in_this_tick = True
            elif eventname == "move down":
                if self.direction != 0:
                    self.direction = 2
                    self.is_there_a_direction_change_in_this_tick = True
            elif eventname == "move right":
                if self.direction != 1:
                    self.direction = 3
                    self.is_there_a_direction_change_in_this_tick = True
            elif eventname == "rotate left":
                self.direction += 1
                if self.direction >= 4:
                    self.direction -= 4
                self.is_there_a_direction_change_in_this_tick = True
            elif eventname == "rotate right":
                self.direction -= 1
                if self.direction < 0:
                    self.direction += 4
                self.is_there_a_direction_change_in_this_tick = True

    def move_snake_if_possible(self):
        if self.direction == 0:
            if self.test_for_type_of_block_in_field(self.heat_x, self.heat_y - 1) <= 1:
                self.heat_y -= 1
            else:
                self.game_over = True
        elif self.direction == 1:
            if self.test_for_type_of_block_in_field(self.heat_x - 1, self.heat_y) <= 1:
                self.heat_x -= 1
            else:
                self.game_over = True
        elif self.direction == 2:
            if self.test_for_type_of_block_in_field(self.heat_x, self.heat_y + 1) <= 1:
                self.heat_y += 1
            else:
                self.game_over = True
        elif self.direction == 3:
            if self.test_for_type_of_block_in_field(self.heat_x + 1, self.heat_y) <= 1:
                self.heat_x += 1
            else:
                self.game_over = True

        if not self.game_over:
            if self.test_for_type_of_block_in_field(self.heat_x, self.heat_y) == -1:  # if heat eat food
                self.food_is_on_field = False
                self.lenght_of_snake += 1
                self.score.score_for_block()
                self.field_matrix.set_all_pixels_to_black()
                self.score.draw_score_on_field(self.field_matrix)
                self.led_matrix_painter.draw(self.field_matrix)
            self.turn_every_pixel_in_snakes_field_ones_up()
            self.field_for_snake[self.heat_y][self.heat_x] = 1
        else:
            game_sound.stop_song()
            game_sound.play_sound("game_over")
            # self.highscorelist.add_entry(Highscoreentry(datetime.today(), self.playername, self.score.get_score_int()))
            # self.highscorelist.save()
            self.led_matrix_painter.show_Message("Game over - Your Points: " + str(self.score.get_score_str()), 250)

    def turn_every_pixel_in_snakes_field_ones_up(self):
        for y in range(len(self.field_for_snake)):
            for x in range(len(self.field_for_snake[0])):
                if self.field_for_snake[y][x] > 0:
                    self.field_for_snake[y][x] += 1
                    if self.field_for_snake[y][x] > self.lenght_of_snake:
                        self.field_for_snake[y][x] = 0

    def test_for_type_of_block_in_field(self, x: int, y: int) -> int:
        if 0 <= x < len(self.field_for_snake[0]) and 0 <= y < len(self.field_for_snake):
            if self.field_for_snake[y][x] == 0:
                return 0  # there is nothing
            elif self.field_for_snake[y][x] < 0:
                return -1  # it's food
            elif self.field_for_snake[y][x] == self.lenght_of_snake:
                return 1  # it's the end of snake, will be away after move
            else:
                return 2  # it's the body of Snake
        else:
            return 3  # not in field

    def translate_snakes_field_into_normal_field(self):
        self.field_leds.set_all_pixels_to_black()
        for y in range(self.field_leds.height):
            for x in range(self.field_leds.width):
                if self.field_for_snake[y][x] == 1:
                    self.field_leds.field[y][x] = [255, 0, 0]
                elif self.field_for_snake[y][x] > 1:
                    self.field_leds.field[y][x] = [0, 255, 0]
                elif self.field_for_snake[y][x] == -1:
                    self.field_leds.field[y][x] = [0, 0, 255]

    def test_and_print_food(self):
        if not self.food_is_on_field:
            while not self.food_is_on_field:
                self.food_x = int(random()*len(self.field_for_snake[0]))
                self.food_y = int(random()*len(self.field_for_snake))
                if self.test_for_type_of_block_in_field(self.food_x, self.food_y) == 0:
                    self.food_is_on_field = True
                    self.field_for_snake[self.food_y][self.food_x] = -1

    def tick(self):
        if not self.game_over:
            self.move_snake_if_possible()
            self.test_and_print_food()
            self.translate_snakes_field_into_normal_field()
            self.rgb_field_painter.draw(self.field_leds)

            self.is_there_a_direction_change_in_this_tick = False
            self.get_delay()
            time.sleep(self.delay)
        else:
            self.led_matrix_painter.move_Message()
            time.sleep(0.02)

    def get_delay(self):
        if self.score.get_score_int() < 4:
            self.delay = 0.5
        elif self.score.get_score_int() < 6:
            self.delay = 0.45
        elif self.score.get_score_int() < 8:
            self.delay = 0.4
        elif self.score.get_score_int() < 10:
            self.delay = 0.35
        elif self.score.get_score_int() < 12:
            self.delay = 0.33
        elif self.score.get_score_int() < 14:
            self.delay = 0.31
        elif self.score.get_score_int() < 16:
            self.delay = 0.28
        elif self.score.get_score_int() < 18:
            self.delay = 0.25
        elif self.score.get_score_int() < 20:
            self.delay = 0.2
        elif self.score.get_score_int() < 30:
            self.delay = 0.15
        else:
            self.delay = 0.1

    def start(self, playername: str = None):
        super().start(playername)
        self.prepare_for_start()

    def stop(self):
        self.game_over = True

    def is_game_over(self):
        return super(Snake_Main, self).is_game_over()

    def prepare_for_start(self):
        self.field_leds.set_all_pixels_to_black()
        self.field_matrix.set_all_pixels_to_black()

        self.field_for_snake = []

        for i in range(self.field_leds.height):
            self.field_for_snake.append([])
            for _ in range(self.field_leds.width):
                self.field_for_snake[i].append(0)

        self.heat_x = 5
        self.heat_y = 20

        self.direction = 0
        self.lenght_of_snake = 3
        self.game_over = False

        self.food_is_on_field = False
        self.food_x = 0
        self.food_y = 0

        self.is_there_a_direction_change_in_this_tick = False

        self.score = Score()
        self.score.points = 3
        self.score.draw_score_on_field(self.field_matrix)
        self.rgb_field_painter.draw(self.field_leds)
        self.led_matrix_painter.draw(self.field_matrix)
