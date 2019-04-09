from block import blocks
from random import random
from array_vervielfachen import Array_Vervielfachen

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        self.generate_field()
        self.colors = [[170, 0, 255], [255, 225, 0], [0, 255, 245], [20, 255, 0], [255, 0, 0], [255, 165, 0], [0, 40, 255]]

    def set_all_pixels_to_black(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.field[y][x] = [0, 0, 0]

    def set_pixel(self, x, y, color):
        self.field[y][x] = self.colors[color]

    def generate_field(self):
        for y in range(0, self.height):
            self.field.append([])
            for x in range(0, self.width):
                self.field[y].append([0, 0, 0])

    def set_block(self, x=0, y=0):
        blocktodraw = blocks[int(random()*7)]
        line_number = 0
        for line in blocktodraw:
            column_number = 0
            for column in line:
                if column != 0:
                    self.set_pixel(column_number+x, line_number+y, blocktodraw[line_number][column_number]-1)
                column_number = column_number+1
            line_number = line_number+1



    def set_block_doppel_size(self, x=0, y=0):
        array_vervielfachen = Array_Vervielfachen()
        blocktodraw = array_vervielfachen.resize_dopple(blocks[int(random()*7)])

