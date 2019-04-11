from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter


class Feature:
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        self.mode = 0
        self.field_leds = field_leds
        self.field_matrix = field_matrix
        self.rgb_field_painter = rgb_field_painter
        self.led_matrix_painter = led_matrix_painter

    def event(self, eventname: str):
        raise NotImplementedError

    def tick(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
