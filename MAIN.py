from clock import Clock
from feature import Feature
from field import Field
from painter import RGB_Field_Painter, Led_Matrix_Painter

field_leds = Field(10, 20)
field_matrix = Field(32, 8)
rgb_field_painter = RGB_Field_Painter()
led_matrix_painter = Led_Matrix_Painter()

clock = Clock(field_leds, rgb_field_painter)
tetris = Feature(field_leds, rgb_field_painter)
snake = Feature(field_leds, rgb_field_painter)
