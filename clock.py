from datetime import datetime
from feature import Feature
from field import Field
from numbersforwatch import Number
from painter import RGB_Field_Painter, Led_Matrix_Painter


class Clock(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Clock, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

    def get_time(self):
        tuple_time = datetime.timetuple(datetime.today())
        return tuple_time[3], tuple_time[4],  tuple_time[5]

    def draw_clock(self):
        self.field_leds.set_all_pixels_to_black()
        hour, minute, second = self.get_time()
        hour_str = ("0"+str(hour))[-2:]
        minute_str = ("0" + str(minute))[-2:]
        second_str = ("0" + str(second))[-2:]

        clock_array = [int(hour_str[0]), int(hour_str[1]),
                       int(minute_str[0]), int(minute_str[1]),
                       int(second_str[0]), int(second_str[1])]
        positions = [[0, 1], [5, 1], [0, 7], [5, 7], [0, 13], [5, 13]]
        for i in range(6):
            digit = clock_array[i]
            self.field_leds.set_block(Number(digit).block, positions[i][0], positions[i][1])

    def event(self, eventname: str):
        if eventname == "rainbow":
            pass
        if eventname == "white":
            pass

    def tick(self):
        self.draw_clock()


if __name__ == "__main__":
    field_leds = Field(10, 20)
    rgb_field_painter = RGB_Field_Painter()
    clock = Clock(field_leds, field_leds, rgb_field_painter, Led_Matrix_Painter())
    while True:
        clock.draw_clock()
        rgb_field_painter.draw(field_leds)
