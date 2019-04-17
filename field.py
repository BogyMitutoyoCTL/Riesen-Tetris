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

    def set_block(self, block_to_draw: Block, field_x: int, field_y: int, color: list = None):
        if color is None:
            color = block_to_draw.color
        self.draw_block(block_to_draw, color, field_x, field_y)

    def remove_block(self, block_to_draw: Block, field_x: int, field_y: int):
        self.draw_block(block_to_draw, BLACK, field_x, field_y)

    def draw_block(self, block_to_draw: Block, color: list, field_x: int, field_y: int):
        for brick_y in range(block_to_draw.height):
            for brick_x in range(block_to_draw.width):
                if block_to_draw.is_brick(brick_x, brick_y):
                    self.set_pixel(brick_x + field_x, brick_y + field_y, color)

    def give_type_of_collision(self, block_to_draw: Block, x: int, y: int) -> int:
        for y_count in range(block_to_draw.height):
            for x_count in range(block_to_draw.width):
                if block_to_draw.is_brick(x_count, y_count):
                    if y + y_count > self.height - 1:
                        print("Kollision Boden", end="")
                        return 1
                    elif x + x_count < 0:
                        print("Kollision linker Rand", end="")
                        return 1
                    elif x + x_count > self.width - 1:
                        print("Kollision rechter Rand", end="")
                        return 1
                    elif not self.pixel_is_inside_field(x + x_count, y_count + y):
                        pass
                    elif self.field[y + y_count][x + x_count] != BLACK:
                        print("Kollision Block", end="")
                        return self.is_hole_block_in_field(block_to_draw, y)
        return 0

    def is_hole_block_in_field(self, block_to_draw: Block, y: int) -> int:
        if self.pixel_is_inside_field(0, y+block_to_draw.get_line_of_first_pixel_from_top()-1): # -1 weil der Block ja eins runtergesetzt wurde
            return 1
        else:
            return 2

    def get_all_full_lines(self) -> list:
        lines_to_delete = []
        for y in range(self.height):
            line_is_full = True
            for x in range(self.width):
                if self.field[y][x] == BLACK:
                    line_is_full = False
                    break

            if line_is_full:
                lines_to_delete.append(y)
        return lines_to_delete

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
