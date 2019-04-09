import numpy
from PIL import Image


class Array_Vervielfachen:
    def resize_dopple(self, array):
        img = Image.fromarray(numpy.array(array))
        img = img.resize((len(array[0])*2, len(array)*2), Image.NEAREST)

        ret = numpy.array(img)
        return ret
