import random

from shapes.core.colors import Colors, get_random_color, get_gradation_between_two_colors
from shapes.core.image import new_image, save_image


class ColoringTypes(object):
    random = 'random'
    rgb_colors = 'rgb_colors'
    rgb_distance = 'rgb_distance'
    gradation_to_white = 'gradation_to_white'


def distance(point_a, point_b):
    return int(((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2) ** 0.5)


def get_random_point(min_x=0, max_x=1080, min_y=0, max_y=1080):
    return random.randint(min_x, max_x), random.randint(min_y, max_y)


def draw_chaos_game(image_width=1080, image_height=1080, polygon_points=None, iterations=10 ** 5,
                    color=Colors.white, coloring_type=None):
    """

    :param image_width: the image width in pixels
    :param image_height: the image height in pixels
    :param polygon_points: a list of polygon points, where each point is a tuple of two numbers.
        In each iteration of the Chaos Game, one of these points will be chosen at random.
    :param iterations: the number of times a new point will be drawn halfway the previous and the random polygon point
    :param color: The color of the point to draw. Should be a tuple with rgb values, like (230, 25, 75)
    :param coloring_type:

    :return: The file path of the image that was created
    """
    if polygon_points is None:
        # default will be 3 (triangle) points: bottom left, bottom right, center top,
        polygon_points = [(0, image_height), (image_width, image_height), (image_width // 2, 0)]

    image, draw = new_image(size=(image_width, image_height))

    # this is the random_start_point, but I call it previous_point, since a new point will be calculated based on this
    previous_point = get_random_point(max_x=image_width, max_y=image_height)
    color_gradations = None
    for i in range(iterations):
        # choose one of the 'polygon_points' at random, then calculate the point halfway in that direction
        random_polygon_point = random.choice(polygon_points)
        previous_point = (
            ((random_polygon_point[0] + previous_point[0]) / 2),
            ((random_polygon_point[1] + previous_point[1]) / 2),
        )

        # only override the 'color' parameter when a color_type is specified
        if coloring_type is not None:
            if coloring_type == ColoringTypes.random:
                color = get_random_color()
            elif coloring_type == ColoringTypes.rgb_colors:
                # results in 3 colors, depending which corner point was chosen
                color = tuple([int(point == random_polygon_point) * 255 for point in polygon_points[:3]])
            elif coloring_type == ColoringTypes.rgb_distance:
                # r, g & b values are determined, based on the distance to start_point a, b & c
                division_factor = int(((image_width + image_height) // 2) / 200)  # 5 works for 1080x1080
                color = (
                    distance(previous_point, polygon_points[0]) // division_factor,
                    distance(previous_point, polygon_points[1]) // division_factor,
                    distance(previous_point, polygon_points[2]) // division_factor,
                )
            elif coloring_type == ColoringTypes.gradation_to_white:
                if color_gradations is None:
                    color_gradations = get_gradation_between_two_colors(
                        color_1=color, color_2=Colors.white, iterations=100)

                distance_from_top = distance(previous_point, polygon_points[2])
                color = color_gradations[int(distance_from_top / 20)]

        draw.point(xy=previous_point, fill=color)

    new_image_path = save_image(image=image, file_name='chaos_game')
    return new_image_path


def draw_sierpinsky_triangles_in_different_colors():
    # default chaos game will be with black dots
    draw_chaos_game(image_width=int(1080 * 1.5), image_height=1080, iterations=5 * 10 ** 5)

    # make one with green dots
    draw_chaos_game(image_width=int(1080 * 1.5), image_height=1080, iterations=5 * 10 ** 5,
                    color=Colors.green)

    # make one where every dot is a random color
    draw_chaos_game(image_width=int(1080 * 1.5), image_height=1080, iterations=5 * 10 ** 5,
                    coloring_type=ColoringTypes.random)

    # make one where the color of the dot is based on which of the 3 starting points was chosen
    draw_chaos_game(image_width=int(1080 * 1.5), image_height=1080, iterations=5 * 10 ** 5,
                    coloring_type=ColoringTypes.rgb_colors)

    # make one where the r, g and b values are based on the distance from the 3 corner points
    draw_chaos_game(image_width=int(1080 * 1.5), image_height=1080, iterations=5 * 10 ** 5,
                    coloring_type=ColoringTypes.rgb_distance)

    # same as the previous one, but now the width and height are twice as big
    draw_chaos_game(image_width=int(1080 * 3), image_height=1080 * 2, iterations=1 * 10 ** 6,
                    coloring_type=ColoringTypes.rgb_distance)

    # draw chaos game with color gradations from black to white
    draw_chaos_game(image_width=int(1080 * 1.5), image_height=1080, iterations=5 * 10 ** 5,
                    coloring_type=ColoringTypes.gradation_to_white, color=Colors.black)


def draw_chaos_games_with_random_points_and_colorings(image_width=1620, image_height=1080, iterations=5 * 10 ** 5):
    """
    Draw chaos game with random points (from 3 to 8 start points). Do the coloring random as well.
    Note that the ColoringTypes were made for the triangle with 3 points. So for 6 gons, the coloring
    will be based on 3 points

    :param image_width:
    :param image_height:
    :param iterations:
    :return:
    """
    color = Colors.black
    coloring_type = None
    if random.random() < 0.5:
        color = random.choice([Colors.black, Colors.red, Colors.purple, Colors.lime, Colors.blue])
    else:
        # use a ColoringType
        coloring_type = random.choice(
            [ColoringTypes.random, ColoringTypes.rgb_colors, ColoringTypes.rgb_distance,
             ColoringTypes.gradation_to_white])

    random_number_of_points = random.randint(3, 8)
    list_of_points = [get_random_point(max_x=image_width, max_y=image_height) for _ in range(random_number_of_points)]

    draw_chaos_game(polygon_points=list_of_points, image_width=image_width, image_height=image_height,
                    iterations=iterations, coloring_type=coloring_type, color=color)


draw_sierpinsky_triangles_in_different_colors()

# Uncomment the code below to draw 100 random chaos games (different shapes and different colors)
# for i in range(100):
#     draw_chaos_games_with_random_points_and_colorings()
