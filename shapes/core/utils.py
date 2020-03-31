from decimal import Decimal
import math


def get_n_gon_points(n, radius, addition_x=None, addition_y=None, rotation=0):
    """
    Return a list of points that lay on a circle of the given radius,
    with an equal distance from each other.

    :param n: number of points on the polygon
    :param radius: polygon points will be drawn on a circle with this radius.
    :param rotation: Decimal in radians: for 180 degrees use math.pi radians
    :return: list of n points for this regular n gon. All points are relative to the centre of the circle
        which is (0, 0). First point is always (0, y), right above the centre point.
    """
    assert n > 1, 'N gon should have more then one points'

    if addition_x is None:
        addition_x = radius

    if addition_y is None:
        addition_y = radius

    phi = Decimal('2') * Decimal(math.pi) / Decimal(n)
    points = []
    for i in range(n):
        new_x = Decimal(math.sin(phi * i + rotation)) * radius
        new_y = Decimal(math.cos(phi * i + rotation)) * radius

        points.append((
            new_x + addition_x,
            new_y + addition_y,
        ))

    return points
