class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = []
        self.generate_field()
        self.colorkey = [[0, 0, 0], [170, 0, 255], [255, 225, 0], [0, 255, 245], [20, 255, 0], [255, 0, 0], [255, 165, 0], [0, 40, 255]]

    def draw_field(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.set_pixel(x, y, 0)

    def set_pixel(self, x, y, color):
        self.field[y][x] = self.colorkey[color]

    def generate_field(self):
        for y in range(0, self.height):
            self.field.append([])
            for x in range(0, self.width):
                self.field[y].append([0, 0, 0])



tetrisfield = Field(10, 20)
tetrisfield.set_pixel(0, 19, 1)

print(tetrisfield.field)
#print(tetrisfield.field[0][2])

