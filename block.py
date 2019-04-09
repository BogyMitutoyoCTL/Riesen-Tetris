import numpy
from PIL import Image

blocks = [

    [[0, 1, 0, 0],
     [1, 1, 1, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

    [[0, 2, 2, 0],
     [0, 2, 2, 0],
     [0, 0, 0, 0],
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


class Block:
    def describe(self):
        for line in self.pixels:
            for column in line:
                if column == 0:
                    print(" ", end="")
                else:
                    print(1, end="")

            print()
        print()

    def __init__(self, pixel: list):
        self.pixels = pixel
        self.height = (len(self.pixels))
        self.width = (len(self.pixels[0]))

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
        img = img.resize((len(self.pixels[0])*2, len(self.pixels)*2), Image.NEAREST)

        ret = numpy.array(img)
        return Block(ret)
