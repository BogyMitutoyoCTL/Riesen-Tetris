import time
from datetime import datetime
from feature import Feature
from field import Field
from numbersforwatch import Number
from painter import RGB_Field_Painter, Led_Matrix_Painter


class Clock(Feature):
    def __init__(self, field_leds: Field, field_matrix: Field, rgb_field_painter: RGB_Field_Painter,
                 led_matrix_painter: Led_Matrix_Painter):
        super(Clock, self).__init__(field_leds, field_matrix, rgb_field_painter, led_matrix_painter)

    @staticmethod
    def __leading_zeros(number: int) -> str:
        return ("0"+str(number))[-2:]

    def get_time(self):
        tuple_time = datetime.timetuple(datetime.today())
        return tuple_time[3], tuple_time[4], tuple_time[5]

    def get_date(self):
        tuple_date = datetime.timetuple(datetime.today())
        return tuple_date[0], tuple_date[1], tuple_date[2]

    def draw_clock(self, color: list = None):
        self.field_leds.set_all_pixels_to_black()
        hour, minute, second = self.get_time()
        hour_str = self.__leading_zeros(hour)
        minute_str = self.__leading_zeros(minute)
        second_str = self.__leading_zeros(second)

        clock_array = [int(hour_str[0]), int(hour_str[1]),
                       int(minute_str[0]), int(minute_str[1]),
                       int(second_str[0]), int(second_str[1])]
        positions = [[0, 1], [5, 1], [0, 7], [5, 7], [0, 13], [5, 13]]
        for i in range(6):
            digit = clock_array[i]
            self.field_leds.set_block(Number(digit).block, positions[i][0], positions[i][1], color)

    def get_date_string(self):
        self.field_matrix.set_all_pixels_to_black()
        _, month, day = self.get_date()
        day_str = self.__leading_zeros(day)
        month_str = self.__leading_zeros(month)
        datetext = day_str + "." + month_str + "."
        return datetext

    def event(self, eventname: str):
        pass

    def tick(self):
        self.draw_clock()
        self.rgb_field_painter.draw(self.field_leds)
        self.led_matrix_painter.show_Text(self.get_date_string())

        time.sleep(0.2)

    def start(self, playername: str = None):
        self.field_leds.set_all_pixels_to_black()
        self.field_matrix.set_all_pixels_to_black()
        self.rgb_field_painter.draw(self.field_leds)
        self.led_matrix_painter.draw(self.field_matrix)

    def stop(self):
        pass

    def is_game_over(self):
        return False
