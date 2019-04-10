from block import Block


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        self.generate_field()
        self.lines_to_delete = []

    def set_all_pixels_to_black(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.field[y][x] = [0, 0, 0]

    def generate_field(self):
        for y in range(0, self.height):
            self.field.append([])
            for x in range(0, self.width):
                self.field[y].append([0, 0, 0])

    def set_pixel(self, x, y, color):
        self.field[y][x] = color

    def set_colorpixel(self, x, y, color):
        self.field[y][x] = color

    def set_block(self, block_to_draw: Block, x, y):
        line_number = 0
        for line in block_to_draw.pixels:
            column_number = 0
            for column in line:
                if column != 0:
                    if line_number + y >= 0:
                        if block_to_draw.pixels[line_number][column_number] > 0:
                            self.set_pixel(column_number + x, line_number + y,
                                           block_to_draw.color)
                column_number = column_number + 1
            line_number = line_number + 1

    def remove_block(self, block_to_draw: Block, x, y):
        line_number = 0
        for line in block_to_draw.pixels:
            column_number = 0
            for column in line:
                if column != 0:
                    if line_number + y >= 0:
                        if block_to_draw.pixels[line_number][column_number] > 0:
                            self.set_pixel(column_number + x, line_number + y, [0, 0, 0])
                column_number = column_number + 1
            line_number = line_number + 1

    def test_for_collision(self, block_to_draw: Block, x, y):
        ret = 0
        line_begin = len(block_to_draw.pixels[0]) - 1
        line_end = 0
        for x_count_pixel in range(0, len(block_to_draw.pixels[0])):
            line_count = 0
            for y_count_pixel in range(0, len(block_to_draw.pixels)):
                if block_to_draw.pixels[y_count_pixel][x_count_pixel] > 0:
                    line_count += 1
            if line_count > 0:
                if line_begin > x_count_pixel:
                    line_begin = x_count_pixel
                if line_end < x_count_pixel:
                    line_end = x_count_pixel

        for y_count in range(0, len(block_to_draw.pixels)):
            for x_count in range(0, len(block_to_draw.pixels[0])):
                if block_to_draw.pixels[y_count][x_count] > 0:
                    if y + y_count < 0:
                        print("Not in field: y=" + str(y_count) + ", x=" + str(x_count))
                    elif y + y_count > self.height - 1:
                        print("Kollision Boden an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        ret += 1
                    elif x + line_begin < 0:
                        print("Kollision linker Rand an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        ret += 1
                    elif x + line_end > self.width - 1:
                        print("Kollision rechter Rand an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        ret += 1
                    elif self.field[y + y_count][x + x_count][0] + self.field[y + y_count][x + x_count][1] + \
                            self.field[y + y_count][x + x_count][2] != 0:
                        print("Kollision Block an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        ret += 1

        return ret

    def test_for_full_lines(self):
        self.lines_to_delete = []
        for y in range(0, self.height):
            counter = 0
            for x in range(0, self.width):
                if self.field[y][x][0] + self.field[y][x][1] + self.field[y][x][2] > 0:
                    counter += 1
            if counter == self.width:
                self.lines_to_delete.append(y)
        self.delete_line(self.lines_to_delete)

    def delete_line(self, lines: list):
        for i in range(0, len(lines)):
            line = lines[i]
            for y in range(line, 0, -1):
                self.field[y] = self.field[y - 1]

            self.field[0] = []
            for _ in range(0, self.width):
                self.field[0].append([0, 0, 0])
