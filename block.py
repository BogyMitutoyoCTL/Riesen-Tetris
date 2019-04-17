import numpy
from PIL import Image
import copy
from rainbow import rainbowcolors
from random import random


class Block:

    def __init__(self, pixel: list, color):
        self.pixels = pixel
        self.height = (len(self.pixels))
        self.width = (len(self.pixels[0]))
        self.color = color

    def rotateleft(self):
        m = numpy.array(self.pixels)
        m = numpy.rot90(m)
        self.pixels = m.tolist()

    def rotateright(self):
        self.rotateleft()
        self.rotateleft()
        self.rotateleft()

    def double_size(self):
        img = Image.fromarray(numpy.array(self.pixels))
        img = img.resize((self.width * 2, self.height * 2), Image.NEAREST)
        ret = numpy.array(img)
        return Block(ret, copy.deepcopy(self.color))

    def clone(self):
        return Block(copy.deepcopy(self.pixels), copy.deepcopy(self.color))

    def get_line_of_first_pixel_from_top(self):
        count = 0
        for y in range(self.height):
            for x in range(0, self.width):
                if self.pixels[y][x] > 0:
                    count += 1
            if count > 0:
                return y
        return 0

    def get_line_of_first_pixel_from_bottom(self):
        count = 0
        for y in range(self.height - 1, -1, -1):
            for x in range(0, self.width):
                if self.pixels[y][x] > 0:
                    count += 1
            if count > 0:
                return y
        return 0

    def is_brick(self, column_number: int, line_number: int):
        return self.pixels[line_number][column_number] != 0


class TetrisBlock(Block):
    blocks = [

        [[0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],

        [[0, 0, 0, 0],
         [0, 2, 2, 0],
         [0, 2, 2, 0],
         [0, 0, 0, 0]],

        [[0, 0, 0, 0],
         [3, 3, 3, 3],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],

        [[0, 4, 0, 0],
         [0, 4, 4, 0],
         [0, 0, 4, 0],
         [0, 0, 0, 0]],

        [[0, 0, 5, 0],
         [0, 5, 5, 0],
         [0, 5, 0, 0],
         [0, 0, 0, 0]],

        [[0, 6, 0, 0],
         [0, 6, 0, 0],
         [0, 6, 6, 0],
         [0, 0, 0, 0]],

        [[0, 0, 7, 0],
         [0, 0, 7, 0],
         [0, 7, 7, 0],
         [0, 0, 0, 0]]]
    block_colors = rainbowcolors(len(blocks))

    @staticmethod
    def get_random_block():
        type = int(random()*len(TetrisBlock.blocks))
        rotation = int(random()*4)
        block = Block(TetrisBlock.blocks[type], TetrisBlock.block_colors[type])
        for i in range(rotation):
            block.rotateright()
        return block
