class Field ():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field[self.width][self.height][3]
        self.colorkey = [[0, 0, 0][170, 0, 255][255, 225, 0][0, 255, 245][20, 255, 0][255, 0, 0][255, 165, 0][0, 40, 255]]


    def draw_field(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                for k in range(0, 3):
                    self.field[j][i][k] = 0

    def set_pixel(self, x, y, color):
        self.field[x][y] = self.colorkey[color]



tetrisfield = Field(20, 10)
