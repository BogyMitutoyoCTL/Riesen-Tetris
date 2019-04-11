from block import Block
from field import Field
from painter import RGB_Field_Painter
from datetime import datetime, date
import time
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

number_colors = [[255, 255, 255], [0, 204, 204], [255, 0, 0], [51, 0, 0], [127, 0, 255], [255, 125, 255], [0, 102, 51],
                 [255, 0, 255], [0, 0, 255], [153, 0, 76]]


class Number:
    def __init__(self, number: int):
        self.pixel = number_pixels[number]
        self.color = number_colors[number]
        self.block = Block(self.pixel, self.color)


class Clock:
    def __init__(self, field_for_clock):
        self.number_list = [Number(0), Number(1), Number(2), Number(3), Number(4), Number(5), Number(6), Number(7),
                            Number(8), Number(9)]
        self.field_for_clock = field_for_clock

    def get_time(self):
        tuple_time = datetime.timetuple(datetime.today())
        print(tuple_time)
        self.hour = tuple_time[3]
        self.minute = tuple_time[4]
        self.second = tuple_time[5]

    def draw_clock(self):
        self.field_for_clock.set_all_pixels_to_black()
        self.get_time()
        self.hour_str = ""
        if self.hour < 10:
            self.hour_str += "0"
        self.hour_str += str(self.hour)

        self.minute_str = ""
        if self.minute < 10:
            self.minute_str += "0"
        self.minute_str += str(self.minute)

        self.second_str = ""
        if self.second < 10:
            self.second_str += "0"
        self.second_str += str(self.second)

        self.clock_array = [int(self.hour_str[0]), int(self.hour_str[1]), int(self.minute_str[0]),
                            int(self.minute_str[1]), int(self.second_str[0]), int(self.second_str[1])]
        self.field_for_clock.set_block(self.number_list[self.clock_array[0]].block, 0, 1)
        self.field_for_clock.set_block(self.number_list[self.clock_array[1]].block, 5, 1)
        self.field_for_clock.set_block(self.number_list[self.clock_array[2]].block, 0, 7)
        self.field_for_clock.set_block(self.number_list[self.clock_array[3]].block, 5, 7)
        self.field_for_clock.set_block(self.number_list[self.clock_array[4]].block, 0, 13)
        self.field_for_clock.set_block(self.number_list[self.clock_array[5]].block, 5, 13)
        time.sleep(0.1)

    #def rainbow_block(self):
        #self.get_time
        #todo rainbow colors for watch


if __name__ == "__main__":
    field_leds = Field(10, 20)
    rgb_field_painter = RGB_Field_Painter()
    clock = Clock(field_leds)
    while True:
        clock.draw_clock()
        rgb_field_painter.draw(field_leds)

