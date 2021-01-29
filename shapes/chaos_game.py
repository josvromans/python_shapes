import random

from shapes.core.colors import Colors
from shapes.core.image import new_image, save_image


def draw_chaos_game(image_width=1080, image_height=1080, polygon_points=None, iterations=10 ** 5, color=Colors.white):
    """

    :param image_width: the image width in pixels
    :param image_height: the image height in pixels
    :param polygon_points: a list of polygon points, where each point is a tuple of two numbers.
        In each iteration of the Chaos Game, one of these points will be chosen at random.
    :param iterations: the number of times a new point will be drawn halfway the previous and the random polygon point
    :param color: The color of the point to draw. Should be a tuple with rgb values, like (230, 25, 75)

    :return: The file path of the image that was created
    """
    if polygon_points is None:
        # default will be 3 (triangle) points: bottom left, bottom right, center top,
        polygon_points = [(0, image_height), (image_width, image_height), (image_width // 2, 0)]

    image, draw = new_image(size=(image_width, image_height))

    # this is the random_start_point, but I call it previous_point, since a new point will be calculated based on this
    previous_point = (random.randint(0, image_width), random.randint(0, image_height))
    for i in range(iterations):
        # choose one of the 'polygon_points' at random, then calculate the point halfway in that direction
        random_polygon_point = random.choice(polygon_points)
        previous_point = (
            ((random_polygon_point[0] + previous_point[0]) / 2),
            ((random_polygon_point[1] + previous_point[1]) / 2),
        )
        draw.point(xy=previous_point, fill=color)

    new_image_path = save_image(image=image, file_name='chaos_game')
    return new_image_path


# draw_chaos_game(image_width=int(1080 * 1.5), image_height=1080, iterations=5 * 10 ** 5)
