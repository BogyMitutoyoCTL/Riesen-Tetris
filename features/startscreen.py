import time

from block import TetrisBlock
from features.feature import Feature
from field import Field
from painter import Led_Matrix_Painter, RGB_Field_Painter


class Startscreen(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Startscreen, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)
        self.current_block = None
        self.block_position_x = 0
        self.block_position_y = 0
        self.new_block()

    def new_block(self):
        self.current_block = TetrisBlock.get_random_block()

        self.block_position_x = 1
        self.block_position_y = -8

    def falling_blocks(self):
        self.field_leds.set_all_pixels_to_black()
        self.field_leds.set_block(self.current_block, self.block_position_x, self.block_position_y)
        self.block_position_y += 1
        if self.block_position_y >= self.field_leds.height:
            self.new_block()

    def tick(self):
        self.led_matrix_painter.show_Text("Tetris")
        self.falling_blocks()
        self.rgb_field_painter.draw(self.field_leds)
        time.sleep(0.1)

    def stop(self):
        pass
