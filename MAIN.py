#!/usr/bin/python3

import signal
import threading
from time import sleep

import redis

from features.snow import Snow
from highscorelist import *
from painter import RGB_Field_Painter
from features.rainbowclock import Clock
from features.rainbowclock import Rainbowclock
from features.snake_main import Snake_Main
from features.startscreen import Startscreen
from features.tetris import Tetris

running = True


def stophandler(signal, stackframe):
    global running
    print("Stop Tetris due to kill signal")
    running = False


signal.signal(signal.SIGTERM, stophandler)


def control(features: dict, events: dict, subscriptions):
    global active
    global username
    global running

    while running:
        sleep(0.1)
        cmd = get_redis_message(subscriptions)
        if cmd in features:
            active.stop()
            active = features[cmd]
            active.start(username)
        elif cmd == "start_highscore":
            # TODO: implement highscore list display
            test = highscorelist_tetris.highscores
            print(test)
        elif cmd in events:
            active.event(events[cmd])


def get_redis_message(subscriptions) -> str:
    global username
    message = subscriptions.get_message()
    if message:
        command = message['data']
        print(command)
        if isinstance(command, (bytes, bytearray)):
            command = str(command, "utf-8")
            if str(message['channel'], "utf-8") == "username":
                # TODO: global variable hack
                username = command
                return ""
            print("Redis command received:", command)
            return command
    return ""


username = ""
redis_client = redis.StrictRedis(host='localhost', port=6379)
subscriptions = redis_client.pubsub()
subscriptions.subscribe('game_action')
subscriptions.subscribe("username")

field_leds = Field(10, 20)
field_matrix = Field(32, 8)
rgb_field_painter = RGB_Field_Painter()
led_matrix_painter = Led_Matrix_Painter()

highscorelist_tetris = Highscorelist("Tetris")
highscorelist_tetris.load()
highscorelist_snake = Highscorelist("Snake")
highscorelist_snake.load()

rainbowclock = Rainbowclock(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
clock = Clock(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
tetris = Tetris(field_leds, field_matrix, rgb_field_painter, led_matrix_painter, highscorelist_tetris)
snake = Snake_Main(field_leds, field_matrix, rgb_field_painter, led_matrix_painter, highscorelist_snake)
startscreen = Startscreen(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
snow = Snow(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

features = {"start_tetris": tetris,
            "tetris_start": tetris,
            "start_clock_rainbow": rainbowclock,
            "start_clock": clock,
            "start_snake": snake,
            "start_screen": startscreen,
            "start_snow": snow}

events = {"action_new_block": "new",
          "action_turn_left": "rotate left",
          "action_turn_right": "rotate right",
          "action_move_left": "move left",
          "action_move_right": "move right",
          "action_soft_down": "move down",
          "action_hard_down": "move down",
          "action_move_down": "move down",
          "action_move_up": "move up",
          "action_pause": "pause"}

active = snow
active.start("")

thread_for_control = threading.Thread(target=control, args=(features, events, subscriptions))
thread_for_control.daemon = True
thread_for_control.start()

while running:
    active.tick()
