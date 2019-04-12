#!/usr/bin/python3

import threading
from pygame.locals import *
import time
import pygame
import random

from clock import Clock
from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter
from rainbowclock import Rainbowclock
from tetris_main import Tetris_Main

running = True


def control():
    global active
    while running:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_t]:  # tetris
            active.stop()
            active = tetris
            active.start()
            control_wait_for_release(K_t)
        elif keys[K_u]:  # uhr
            active.stop()
            active = clock
            active.start()
            control_wait_for_release(K_u)
        elif keys[K_n]:  # neuer Block    # todo: später rauswerfen (Johannes)
            active.event("new")
            control_wait_for_release(K_n)
        elif keys[K_q]:  # rotate left
            active.event("rotate left")
            control_wait_for_release(K_q)
        elif keys[K_e]:  # rotate right
            active.event("rotate right")
            control_wait_for_release(K_e)
        elif keys[K_a]:  # move left
            active.event("move left")
            control_wait_for_release(K_a)
        elif keys[K_d]:  # move right
            active.event("move right")
            control_wait_for_release(K_d)
        elif keys[K_s]:  # move down
            active.event("move down")
            control_wait_for_release(K_s)


def control_wait_for_release(key):
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    while keys[key]:
        pygame.event.pump()
        keys = pygame.key.get_pressed()


field_leds = Field(10, 20)
field_matrix = Field(32, 8)
rgb_field_painter = RGB_Field_Painter()
led_matrix_painter = Led_Matrix_Painter()

clock = Rainbowclock(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
tetris = Tetris_Main(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

features = [tetris, clock]

active = features[0]
active.start()

thread_for_control = threading.Thread(target=control)
thread_for_control.daemon = True
thread_for_control.start()

while True:
    active.tick()
