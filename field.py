from block import blocks
from random import random

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        self.generate_field()
        self.colorkey = [[0, 0, 0], [170, 0, 255], [255, 225, 0], [0, 255, 245], [20, 255, 0], [255, 0, 0], [255, 165, 0], [0, 40, 255]]

    def set_all_pixels_to_black(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.set_pixel(x, y, 0)

    def set_pixel(self, x, y, color):
        self.field[y][x] = self.colorkey[color]

    def generate_field(self):
        for y in range(0, self.height):
            self.field.append([])
            for x in range(0, self.width):
                self.field[y].append([0, 0, 0])

    def set_block(self):
        blocktodraw = blocks[int(random()*7)]
        y = 0
        for line in blocktodraw:
            x = 3
            for column in line:
                if column != 0:
                    self.set_pixel(x, y, blocktodraw[y][x-3])
                x = x+1
            y = y+1
