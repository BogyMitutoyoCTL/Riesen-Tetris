import numpy
from PIL import Image

from rainbow import rainbowcolors

# TODO: hierauf hat jeder Zugriff
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

# TODO: hierauf hat jeder Zugriff
block_colors = rainbowcolors(7)


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
        return Block(ret, self.color)

    def get_rotated_left(self):
        # TODO: Was bedeutet m?
        m = numpy.array(self.pixels)
        m = numpy.rot90(m)
        ret = m.tolist()
        return ret

    def get_rotated_right(self):
        m = numpy.array(self.pixels)
        m = numpy.rot90(m)
        m = numpy.rot90(m)
        m = numpy.rot90(m)
        ret = m.tolist()
        return ret

    def get_line_of_first_pixel_from_top(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.is_brick(x, y):
                    count += 1
            if count > 0:
                return y
        return 0

    def get_line_of_first_pixel_from_bottom(self):
        count = 0
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if self.is_brick(x, y):
                    count += 1
            if count > 0:
                return y
        return 0

    def get_line_of_first_pixel_from_left(self):
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.is_brick(x, y):
                    count += 1
            if count > 0:
                return x
        return 0

    def get_line_of_first_pixel_from_right(self):
        count = 0
        for x in range(self.width - 1, -1, -1):
            for y in range(self.height):
                if self.is_brick(x, y):
                    count += 1
            if count > 0:
                return x
        return 0

    def is_brick(self, column_number: int, line_number: int):
        return self.pixels[line_number][column_number] != 0
