import threading
from pygame.locals import *
import time
import pygame

from clock import Clock
from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter
from tetris_main import Tetris_Main


def control():
    while True:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_n]:  # neuer Block    # todo: später rauswerfen (Johannes)
            tetris.event("new")
            control_wait_for_release(K_n)
        elif keys[K_q]:  # rotate left
            tetris.event("rotate left")
            control_wait_for_release(K_q)
        elif keys[K_e]:  # rotate right
            tetris.event("rotate right")
            control_wait_for_release(K_e)
        elif keys[K_a]:  # move left
            tetris.event("move left")
            control_wait_for_release(K_a)
        elif keys[K_d]:  # move right
            tetris.event("move right")
            control_wait_for_release(K_d)
        elif keys[K_s]:  # move down
            tetris.event("move down")
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

clock = Clock(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
tetris = Tetris_Main(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

input()
tetris.start()
input()

thread_for_control = threading.Thread(target=control)  # ohne () nach target=tetris_main.control
thread_for_control.daemon = True
thread_for_control.start()

while True:
    tetris.tick()
    time.sleep(tetris.delay)

input()
