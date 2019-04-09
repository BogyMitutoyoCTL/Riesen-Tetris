from block import Block
from block import block_colors
from block import number_colors

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        self.generate_field()


    def set_all_pixels_to_black(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.field[y][x] = [0, 0, 0]

    def set_pixel(self, x, y, color):
        self.field[y][x] = block_colors[color]

    def generate_field(self):
        for y in range(0, self.height):
            self.field.append([])
            for x in range(0, self.width):
                self.field[y].append([0, 0, 0])

    def set_colorpixel(self, x, y, color):
        self.field[y][x] = color

    def set_block(self, block_to_draw: Block, x=3, y=0):
        line_number = 0
        for line in block_to_draw.pixels:
            column_number = 0
            for column in line:
                if column != 0:
                    if block_to_draw.pixels[line_number][column_number] > 0:
                        self.set_pixel(column_number + x, line_number + y,
                                       block_to_draw.pixels[line_number][column_number] - 1)
                column_number = column_number + 1
            line_number = line_number + 1

    #def test_for_collision(self, block_to_draw: Block, x=3, y=0):

    def remove_block(self, block_to_draw: Block, x=3, y=0):
        line_number = 0
        for line in block_to_draw.pixels:
            column_number = 0
            for column in line:
                if column != 0:
                    if block_to_draw.pixels[line_number][column_number] > 0:
                        self.set_pixel(column_number + x, line_number + y, 7)
                column_number = column_number + 1
            line_number = line_number + 1

    def set_number_pixel(self, x, y, color):
        self.field[y][x] = number_colors[color]

    def set_number(self, number_to_draw: Block, x=3, y=0):
        line_number = 0
        for line in number_to_draw.pixels:
            column_number = 0
            for column in line:
                if column != 0:
                    if number_to_draw.pixels[line_number][column_number] > 0:
                        self.set_number_pixel(column_number + x, line_number + y,
                                       number_to_draw.pixels[line_number][column_number] - 1)
                column_number = column_number + 1
            line_number = line_number + 1
