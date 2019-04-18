import time

from PIL import Image

from features.feature import Feature


class Mona(Feature):

    def __init__(self, field_leds, field_matrix, rgb_field_painter, led_matrix_painter):
        super(Mona, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

    def event(self, eventname: str):
        pass

    def tick(self):
        im = Image.open("./image-files/mona.png")
        data = im.getdata()
        for y in range(20):
            for x in range(10):
                self.field_leds.set_pixel(x, y, data[y*10+x])
        self.rgb_field_painter.draw(self.field_leds)
        time.sleep(0.2)

    def stop(self):
        pass