from field import Field


class Painter:
    # def __init__(self):

    # def led_field(self):

    def console(self, field_to_print: Field):
        print("Feldbreite: " + str(field_to_print.width) + "; Höhe: " + str(field_to_print.height))
        text = ""
        for j in range(0, field_to_print.height):
            for i in range(0, field_to_print.width):
                if (field_to_print.field[j][i][0] + field_to_print.field[j][i][1] + field_to_print.field[j][i][2]) > 0:
                    text += "x"
                else:
                    text += "_"
            text += "\n"
        print(text)
        print("--------------------------")


tetrisfield = Field(20, 10)

painter = Painter()
painter.console(tetrisfield)

tetrisfield.field[0][0][0]=1

painter.console(tetrisfield)
