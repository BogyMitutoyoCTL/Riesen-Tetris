from random import random

from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter, Console_Painter
from block import Block, blocks


field_leds = Field(10, 20)
field_matrix = Field(32, 8)

rgb_field_painter = RGB_Field_Painter()
led_matrix_painter = Led_Matrix_Painter()

block = Block(blocks[2])

while True:
    field_leds.set_block(block, 6, 10)
    rgb_field_painter.draw(field_leds)

    field_matrix.set_block(block.double_size(), 24, 0)
    led_matrix_painter.draw(field_matrix)

    input()

    #block = Block(blocks[int(random()*6)])
    block.rotateright()

    field_leds.set_all_pixels_to_black()
    field_matrix.set_all_pixels_to_black()
