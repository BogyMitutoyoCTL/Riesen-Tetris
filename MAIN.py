#!/usr/bin/python3

import threading

import redis
from pygame.locals import *
from rainbowclock import Clock
from painter import RGB_Field_Painter
from rainbowclock import Rainbowclock
from snake_main import Snake_Main
from tetris_main import Tetris_Main
from startscreen import Startscreen
from highscorelist import *

running = True
startscreen_default = "start_startscreen_snow"


def control():
    global active
    global username
    global startscreen_default
    while running:
        cmd = get_redis_message()
        if cmd == "start_tetris":  # tetris
            active.stop()
            active = tetris
            active.start(username)
        elif cmd == "start_clock":  # uhr
            active.stop()
            active = clock
            active.start()
        elif cmd == "start_snake":  # snake
            active.stop()
            active = snake
            active.start()
        elif cmd == "start_startscreen":  # start default one
            chose_startscreen()
        elif cmd == "start_startscreen_snow":  # startscreen snow
            startscreen_default = cmd
            chose_startscreen()
        elif cmd == "start_startscreen_falling_blocks":  # startscreen falling_blocks
            startscreen_default = cmd
            chose_startscreen()
        elif cmd == "start_startscreen_rainbow_clock":  # rainbow uhr
            startscreen_default = cmd
            chose_startscreen()
        elif cmd == "start_startscreen_clock":  # uhr
            startscreen_default = cmd
            chose_startscreen()
        elif cmd == "start_highscore":  # Highscorelist
            test = highscorelist_tetris.highscores
            print(test)
        elif cmd == "action_new_block":  # neuer Block    # todo: später rauswerfen (Johannes)
            active.event("new")
        elif cmd == "action_turn_left":  # rotate left
            active.event("rotate left")
        elif cmd == "action_turn_right":  # rotate right
            active.event("rotate right")
        elif cmd == "action_move_left":  # move left
            active.event("move left")
        elif cmd == "action_move_right":  # move right
            active.event("move right")
        elif cmd == "action_soft_down":  # move soft down
            active.event("move down")
        elif cmd == "action_hard_down":  # move hard down
            active.event("move down")
        elif cmd == "action_move_down":  # move down
            active.event("move down")
        elif cmd == "action_move_up":  # move up
            active.event("move up")
        elif cmd == "action_pause":
            pass

def chose_startscreen():
    global active
    global startscreen_default
    if startscreen_default == "start_startscreen_snow":
        active.stop()
        active = startscreen
        active.start(mode="snow")
    elif startscreen_default == "start_startscreen_falling_blocks":
        active.stop()
        active = startscreen
        active.start(mode="falling_blocks")
    elif startscreen_default == "start_startscreen_rainbow_clock":
        active.stop()
        active = rainbowclock
        active.start()
    elif startscreen_default == "start_startscreen_clock":
        active.stop()
        active = clock
        active.start()


def get_redis_message() -> str:
    global p
    global username
    message = p.get_message()
    if message:
        command = message['data']
        if isinstance(command, (bytes, bytearray)):
            command = str(command, "utf-8")
            if str(message['channel'], "utf-8") == "username":
                username = command
                return ""
            print("Redis command received:", command)
            return command
    return ""


username = ""
r = redis.StrictRedis(host='localhost', port=6379)
p = r.pubsub()
p.subscribe('game_action')
p.subscribe("username")

field_leds = Field(10, 20)
field_matrix = Field(32, 8)
rgb_field_painter = RGB_Field_Painter()
led_matrix_painter = Led_Matrix_Painter()

highscorelist_tetris = Highscorelist("Tetris")
highscorelist_tetris.load()

rainbowclock = Rainbowclock(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
clock = Clock(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
tetris = Tetris_Main(field_leds, field_matrix, rgb_field_painter, led_matrix_painter, highscorelist_tetris)
snake = Snake_Main(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
startscreen = Startscreen(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

active = rainbowclock
active.start()

thread_for_control = threading.Thread(target=control)
thread_for_control.daemon = True
thread_for_control.start()

while True:
    active.tick()
