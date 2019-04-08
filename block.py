blocks = [

    [[0, 1, 0, 0],
     [1, 1, 1, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

    [[0, 0, 0, 0],
     [0, 2, 2, 0],
     [0, 2, 2, 0],
     [0, 0, 0, 0]],

    [[3, 3, 3, 3],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

    [[4, 0, 0, 0],
     [4, 4, 0, 0],
     [0, 4, 0, 0],
     [0, 0, 0, 0]],

    [[0, 5, 0, 0],
     [5, 5, 0, 0],
     [5, 0, 0, 0],
     [0, 0, 0, 0]],

    [[0, 6, 0, 0],
     [0, 6, 0, 0],
     [0, 6, 6, 0],
     [0, 0, 0, 0]],

    [[0, 7, 0, 0],
     [0, 7, 0, 0],
     [7, 7, 0, 0],
     [0, 0, 0, 0]]]


class Block:
    def describe(self):
        for line in self.pixel:
            for column in line:
                if column == 0:
                    print(" ", end="")
                else:
                    print(1, end="")

            print()

    def __init__(self, pixel):
        self.pixel = pixel
        self.height = (len(self.pixel))
        self.width = (len(self.pixel[0]))

    def rotate(self):
        result = []
        for w in range(self.width):
            result.append([])
            for h in range(self.height):
                p = self.pixel[h][w]
                result[w].append(p)
        self.pixel = result










a = Block(blocks[0])
a.describe()
a.rotate()
a.describe()
a.rotate()
a.describe()
