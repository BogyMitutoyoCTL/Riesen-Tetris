from block import Block
from rainbow import rainbowcolors

number_pixels = [

    [[1, 1, 1, 1],
     [1, 0, 0, 1],
     [1, 0, 0, 1],
     [1, 0, 0, 1],
     [1, 1, 1, 1]],

    [[0, 0, 2, 0],
     [0, 0, 2, 0],
     [0, 0, 2, 0],
     [0, 0, 2, 0],
     [0, 0, 2, 0]],

    [[3, 3, 3, 3],
     [0, 0, 0, 3],
     [3, 3, 3, 3],
     [3, 0, 0, 0],
     [3, 3, 3, 3]],

    [[4, 4, 4, 4],
     [0, 0, 0, 4],
     [0, 4, 4, 4],
     [0, 0, 0, 4],
     [4, 4, 4, 4]],

    [[5, 0, 0, 5],
     [5, 0, 0, 5],
     [5, 5, 5, 5],
     [0, 0, 0, 5],
     [0, 0, 0, 5]],

    [[6, 6, 6, 6],
     [6, 0, 0, 0],
     [6, 6, 6, 6],
     [0, 0, 0, 6],
     [6, 6, 6, 6]],

    [[7, 7, 7, 7],
     [7, 0, 0, 0],
     [7, 7, 7, 7],
     [7, 0, 0, 7],
     [7, 7, 7, 7]],

    [[8, 8, 8, 8],
     [0, 0, 0, 8],
     [0, 0, 0, 8],
     [0, 0, 0, 8],
     [0, 0, 0, 8]],

    [[9, 9, 9, 9],
     [9, 0, 0, 9],
     [9, 9, 9, 9],
     [9, 0, 0, 9],
     [9, 9, 9, 9]],

    [[10, 10, 10, 10],
     [10, 0, 0, 10],
     [10, 10, 10, 10],
     [0, 0, 0, 10],
     [10, 10, 10, 10]]
]

number_colors = rainbowcolors(10)


class Number:
    def __init__(self, number: int):
        self.pixel = number_pixels[number]
        self.color = number_colors[number]
        self.block = Block(self.pixel, self.color)
