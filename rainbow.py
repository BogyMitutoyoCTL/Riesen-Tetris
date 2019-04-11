import colorsys


def hsv2rgb(h: float, s: float, v: float):
    return tuple(round(i*255)for i in colorsys.hsv_to_rgb(h, s, v))


def rainbowcolors(howmany: int):
    colors = []
    for i in range(howmany):
        colors.append(hsv2rgb(i/howmany, 1, 1))
    return colors

