import random
from decimal import Decimal

from shapes.core.image import new_image, save_image


def get_next_polygon_points(polygon_points, percentage):
    """
    Look at every pair of polygon points that follow each other:
    which is every line in the polygon.

    Call the two points in every line point_a and point_b.
    There is also a line from the last point in the list to the first point in the list.

    Calculate the next point based on the percentage and the difference between x and y values of two points.
    """
    next_points = []
    for index in range(len(polygon_points)):
        point_a = polygon_points[index]
        # modulo len(points) will make sure the last index + 1 will be zero.
        point_b = polygon_points[(index + 1) % len(polygon_points)]

        diff_x = point_b[0] - point_a[0]
        diff_y = point_b[1] - point_a[1]

        next_x = point_a[0] + percentage * diff_x
        next_y = point_a[1] + percentage * diff_y

        next_points.append((next_x, next_y))

    return next_points


def draw_pursuit_curve(image_width=1080, image_height=1080, iterations=30, percentage=Decimal('0.5'), margin=20):
    image, draw = new_image(size=(image_width, image_height))

    # The four corner points of a square, by taking the image dimensions and margin into account
    n_gon_points = [
        (margin, margin),
        (image_width - margin, margin),
        (image_width - margin, image_height - margin),
        (margin, image_height - margin)
    ]

    for i in range(iterations):
        draw.polygon(xy=n_gon_points)
        n_gon_points = get_next_polygon_points(polygon_points=n_gon_points, percentage=percentage)

    save_image(image=image, file_name='pursuit_curve')


def draw_random_pursuit_curve(n=4, image_width=1080, image_height=1080, iterations=30, percentage=Decimal('0.05')):
    image, draw = new_image(size=(image_width, image_height))

    n_gon_points = [(random.randint(0, image_width), random.randint(0, image_height)) for _ in range(n)]
    for i in range(iterations):
        draw.polygon(xy=n_gon_points)
        n_gon_points = get_next_polygon_points(polygon_points=n_gon_points, percentage=percentage)

    save_image(image=image, file_name='pursuit_curve_random', resize_size=(1080, 1080))

# draw a regular pursuit square
# draw_pursuit_curve(iterations=100, percentage=Decimal(0.03))


# draw random pursuit polygons with 3, 4, 5 and 6 corner points
# for n in range(3, 7):
#     draw_random_pursuit_curve(
#         n=n, image_width=5000, image_height=5000,
#         iterations=500, percentage=Decimal(6 / 1000),
#     )
