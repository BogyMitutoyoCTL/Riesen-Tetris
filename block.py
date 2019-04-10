import numpy
from PIL import Image

blocks = [

    [[0, 1, 0, 0],
     [1, 1, 1, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

    [[0, 0, 0, 0],
     [0, 2, 2, 0],
     [0, 2, 2, 0],
     [0, 0, 0, 0]],

    [[3, 3, 3, 3],
     [0, 0, 0, 0],
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

block_colors = [[170, 0, 255], [255, 225, 0], [0, 255, 245], [20, 255, 0], [255, 0, 0], [255, 165, 0],
                [0, 40, 255]]


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
