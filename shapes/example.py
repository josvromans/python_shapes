from shapes.core.animation import make_movie
from shapes.core.image import new_image, save_image


def draw_trapezoid(image_width=1080, image_height=1080, extra_margin=0, margin=20, line_width=7):
    """
    Generate an image of a four sided shape, that will be a trapezoid if the 'margin' and 'extra_margin'
    are chosen correctly.

    The points are calculated according to the image below. The 'margin' will be calculated from the
    boundary of the image (which is at position 0 or image_height or image_width). The 'extra_margin'
    will only be applied on point A and B.

    For example: the x coordinate of point A will get a total margin on the left of 'margin' plus 'extra_margin'.
    The margin on the top will be 'margin'.

    When the extra margin increases, point A and B will move towards each other.
    At one point, they will overlap and a triangle will be drawn. When the extra_margin increases even more,
    point A and point B will take each others place, and lines AD and BC will intersect.

        Note that the origin, the (0, 0) point, is on the top left.
    (0,0)______________________________________________________________________
        |                                ^                                     |
        |                                | margin                              |
        |                                |                                     |
        |extra_margin<---> ______________v____________________<---> extra_margin
        |                 | A                             B  ﹨                |
        |                |                                    ﹨               |
        |               |                                      ﹨              |
        |              |                                        ﹨             |
        |             |                                          ﹨            |
        |            |____________________________________________﹨           |
        |           D                    ^                         C           |
        |   margin                       | margin                  <---------->|
        |<---------->                    |                           margin    |
        |________________________________v_____________________________________|

    """
    image, draw = new_image(size=(image_width, image_height))

    point_a = (margin + extra_margin, margin)
    point_b = (image_width - margin - extra_margin, margin)
    point_c = (image_width - margin, image_height - margin)
    point_d = (margin, image_height - margin)

    # when a list of several points is given, a multi line will be drawn.
    draw.line(xy=[point_a, point_b, point_c, point_d, point_a], width=line_width, joint='curve')

    save_image(image=image, file_name='trapezoid_margin{}_extra_margin{}'.format(margin, extra_margin))


def draw_a_few_four_gons():
    """
    Use the 'draw_trapezoid' method to draw several polygons.
    Depending on the margin, it can be a square a triangle, trapezoid or something else.
    """
    # with the default parameters, a square is drawn
    draw_trapezoid()

    # when i increase the default width with 50%, it will be a rectangle
    draw_trapezoid(image_width=1620, image_height=1080)

    # when an extra margin of 400 is added, the top of the trapezoid will have length 800 less then the bottom
    draw_trapezoid(image_width=1620, image_height=1080, extra_margin=400)

    # When the 'extra_margin' equals (image_width / 2) - margin, the top line will have length zero.
    draw_trapezoid(image_width=1620, image_height=1080, extra_margin=790)  # a triangle will be drawn

    # the extra margin is 2 x 790 from the previous triangle
    draw_trapezoid(image_width=1620, image_height=1080, extra_margin=1580)


def make_movie_shrinking_trapezoid():
    """
    Make a series of trapezoids, with a fixed extra margin. Iterate over the 'margin' parameter
    so the shape 'sort of shrinks'. The trapezoid gets smaller and smaller and at one point the top line
    will have length 0 (a triangle is visible). After that point, the lines will intersect.
    Also iterate backwards, so the series ends where it began.
    """
    for margin in list(range(0, 410, 4)) + list(range(410, 0, -4)):
        draw_trapezoid(margin=margin, extra_margin=250)

    make_movie(name='shrinking_trapezoid')


def make_movie_dancing_trapezoid(image_width=1080):
    """
    Let the margin increase from 0 to the image_width, but then, draw every image again in descending order.

    One large difference compared to the 'make_movie_shrinking_trapezoid':
    When the total margin is larger then the image_width, the point will be draw outside the image.
    To prevent this, the extra_margin will be recalculated in this case.

    Can you imagine by looking at this code how the animation will look like?

    Note: currently, every image will be generated twice, so that the animation will go end at the start point.
    You can look into ffmpeg and let it make a video reversed, and then merge the original and reversed video.
    """
    margin_range = list(range(0, image_width, 4))
    margin_range = margin_range + margin_range[::-1]  # add the same range to itself, but reversed

    for margin in margin_range:
        extra_margin = margin
        if extra_margin + margin > image_width:
            extra_margin = 2 * image_width - 3 * margin

        draw_trapezoid(image_width=1080, margin=margin, extra_margin=extra_margin)

    make_movie(name='dancing_trapezoid')


# draw_a_few_four_gons()
# make_movie_shrinking_trapezoid()
# make_movie_dancing_trapezoid()
