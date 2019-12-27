import random


class Colors(object):
    """
    RGB colors are specified with a value from 0 - 255 for Red, Green and Blue
    """
    black = (0, 0, 0)
    white = (255, 255, 255)

    blue = (0, 130, 200)
    cyan = (70, 240, 240)
    navy = (0, 0, 128)
    teal = (0, 128, 128)
    purple = (145, 30, 180)
    magenta = (240, 50, 230)
    lavender = (230, 190, 25)
    grey = (128, 128, 128)
    green = (10, 180, 10)
    mint = (170, 255, 195)
    lime = (210, 245, 60)
    olive = (128, 128, 0)
    yellow = (255, 225, 25)
    beige = (255, 250, 200)
    apricot = (255, 215, 180)
    orange = (245, 130, 48)
    brown = (170, 110, 40)
    maroon = (128, 0, 0)
    red = (255, 0, 0)
    pink = (250, 190, 190)


def get_random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def get_gradation_between_two_colors(iterations, color_1=None, color_2=None):
    """
    Return a list of color gradations between color_1 and color_2 in equal steps, and include both the
    start and end color.

    Hint: in case you are not satisfied with the gradation, you might want to look into rgb color values,
    and decide that you don't want to have linear steps in the gradation.

    :param iterations: the length of the list of colours that will be returned, the total number of gradations
    :param color_1: tuple with rgb values like (255, 0, 0) or Colors.red. When None, a random color will be chosen
    :param color_2: tuple with rgb values like (255, 0, 0) or Colors.red. When None, a random color will be chosen
    :return: list of tuples, where each tuple represents a color
    """
    if color_1 is None:
        color_1 = get_random_color()
    if color_2 is None:
        color_2 = get_random_color()

    # calculate the differences in red, green and blue values. Note that these values will be a float,
    # and when calculating the final color, the values will be converted back to integers.
    # divide by (iterations - 1) so that the last calculated value (approximately) equals color_2
    diff_red = (color_1[0] - color_2[0]) / (iterations - 1)
    diff_green = (color_1[1] - color_2[1]) / (iterations - 1)
    diff_blue = (color_1[2] - color_2[2]) / (iterations - 1)

    return [
        (int(color_1[0] - diff_red * i),
         int(color_1[1] - diff_green * i),
         int(color_1[2] - diff_blue * i)) for i in range(iterations)
    ]
