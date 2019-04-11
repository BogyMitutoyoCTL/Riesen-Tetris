from block import Block

BLACK = [0, 0, 0]


class Field:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        self.generate_field()

    def set_all_pixels_to_black(self):
        for y in range(self.height):
            for x in range(self.width):
                self.field[y][x] = BLACK

    def generate_field(self):
        for y in range(self.height):
            self.field.append([])  # empty line
            for x in range(self.width):
                self.field[y].append(BLACK)

    def set_pixel(self, x: int, y: int, color: list):
        if self.pixel_is_inside_field(x, y):
            self.field[y][x] = color

    def set_block(self, block_to_draw: Block, field_x: int, field_y: int):
        self.draw_block(block_to_draw, block_to_draw.color, field_x, field_y)

    def remove_block(self, block_to_draw: Block, field_x: int, field_y: int):
        self.draw_block(block_to_draw, BLACK, field_x, field_y)

    def draw_block(self, block_to_draw: Block, color: list, field_x: int, field_y: int):
        for brick_y in range(block_to_draw.height):
            for brick_x in range(block_to_draw.width):
                if block_to_draw.is_brick(brick_x, brick_y):
                    self.set_pixel(brick_x + field_x, brick_y + field_y, color)

    def collision_count(self, block_to_draw: Block, x: int, y: int) -> int:
        collision_count = 0
        # TODO: Warum muss das rechts anfangen?
        column_begin = block_to_draw.width - 1
        column_end = 0
        # TODO: kann das der Block selbst wissen?
        for x_count_pixel in range(block_to_draw.width):
            column_count = 0
            for y_count_pixel in range(block_to_draw.height):
                if block_to_draw.is_brick(x_count_pixel, y_count_pixel):
                    column_count += 1
            if column_count > 0:
                if column_begin > x_count_pixel:
                    column_begin = x_count_pixel
                if column_end < x_count_pixel:
                    column_end = x_count_pixel

        for y_count in range(block_to_draw.height):
            for x_count in range(block_to_draw.width):
                if block_to_draw.is_brick(x_count, y_count):
                    if y + y_count > self.height - 1:
                        print("Kollision Boden an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        collision_count += 1
                    elif not self.pixel_is_inside_field(0, y_count + y):
                        print("Not in field: y=" + str(y_count) + ", x=" + str(x_count))
                    elif x + column_begin < 0:
                        print("Kollision linker Rand an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        collision_count += 1
                    elif x + column_end > self.width - 1:
                        print("Kollision rechter Rand an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        collision_count += 1
                        # §CT
                    elif self.field[y + y_count][x + x_count][0] + self.field[y + y_count][x + x_count][1] + \
                            self.field[y + y_count][x + x_count][2] != 0:
                        print("Kollision Block an Block.pixel: x=" + str(x_count) + ", y=" + str(y_count))
                        collision_count += 1

        return collision_count

    def delete_all_full_lines(self):
        lines_to_delete = []
        for y in range(self.height):
            line_is_full = True
            for x in range(self.width):
                # §CT
                if self.field[y][x] == BLACK:
                    line_is_full = False
                    break

            if line_is_full:
                lines_to_delete.append(y)
        self.delete_lines(lines_to_delete)

    def delete_lines(self, lines: list):
        for i in range(len(lines)):
            line = lines[i]
            for y in range(line, 0, -1):
                self.field[y] = self.field[y - 1]


            self.field[0] = []
            for _ in range(self.width):
                self.field[0].append(BLACK)

    def pixel_is_inside_field(self, x: int, y: int):
        return 0 <= y < self.height and 0 <= x < self.width
