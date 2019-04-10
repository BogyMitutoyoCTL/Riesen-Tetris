from block import Block
from field import Field
from painter import RGB_Field_Painter
number_pixels = [

    [[1, 1, 1, 1],
     [1, 0, 0, 1],
     [1, 0, 0, 1],
     [1, 0, 0, 1],
     [1, 1, 1, 1]],

    [[0, 2, 0, 0],
     [0, 2, 0, 0],
     [0, 2, 0, 0],
     [0, 2, 0, 0],
     [0, 2, 0, 0]],

    [[3, 3, 3, 3],
     [0, 0, 0, 3],
     [3, 3, 3, 3],
     [3, 0, 0, 0],
     [3, 3, 3, 3]],

    [[4, 4, 4, 4],
     [0, 0, 0, 4],
     [0, 4, 4, 4],
     [0, 0, 0, 4],
     [4, 4, 4, 4]],

    [[5, 0, 0, 5],
     [5, 0, 0, 5],
     [5, 5, 5, 5],
     [0, 0, 0, 5],
     [0, 0, 0, 5]],

    [[6, 6, 6, 6],
     [6, 0, 0, 0],
     [6, 6, 6, 6],
     [0, 0, 0, 6],
     [6, 6, 6, 6]],

    [[7, 7, 7, 7],
     [7, 0, 0, 0],
     [7, 7, 7, 7],
     [7, 0, 0, 7],
     [7, 7, 7, 7]],

    [[8, 8, 8, 8],
     [0, 0, 0, 8],
     [0, 0, 0, 8],
     [0, 0, 0, 8],
     [0, 0, 0, 8]],

    [[9, 9, 9, 9],
     [9, 0, 0, 9],
     [9, 9, 9, 9],
     [9, 0, 0, 9],
     [9, 9, 9, 9]],

    [[10, 10, 10, 10],
     [10, 0, 0, 10],
     [10, 10, 10, 10],
     [0, 0, 0, 10],
     [10, 10, 10, 10]]
]

number_colors = [[255, 255, 255], [51, 255, 255], [255, 0, 0], [50, 255, 50], [127, 0, 255], [255, 255, 0], [0, 255, 0],
                 [255, 0, 255], [0, 153, 0], [255, 135, 0]]


class Number:

    def __init__(self, number: int):
        self.pixel = number_pixels[number]
        self.color = number_colors[number]
        self.block = Block(self.pixel, self.color)

zero = Number(0)
one = Number(1)
two = Number(2)
three = Number(3)


field_leds = Field(10, 20)
rgb_field_painter = RGB_Field_Painter()

field_leds.set_block(two.block, 0, 1)
field_leds.set_block(two.block, 5, 1)
field_leds.set_block(two.block, 0, 7)
field_leds.set_block(two.block, 5, 7)
field_leds.set_block(two.block, 0, 13)
field_leds.set_block(two.block, 5, 13)
rgb_field_painter.draw(field_leds)

input()