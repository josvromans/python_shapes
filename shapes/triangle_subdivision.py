from shapes.core.colors import Colors
from shapes.core.image import new_image, save_image


def get_midpoint(point_a, point_b):
    return(
        (point_a[0] + point_b[0]) / 2,
        (point_a[1] + point_b[1]) / 2,
    )


def divide(triangle_vertices, iteration, strategy):
    index_to_subdivide = strategy[iteration % len(strategy)]
    subdivide_vertex = triangle_vertices.pop(index_to_subdivide)
    midpoint = get_midpoint(*triangle_vertices)  # midpoint of the remaining two triangle_vertices

    return [
        [subdivide_vertex, midpoint, triangle_vertices[0]],
        [subdivide_vertex, midpoint, triangle_vertices[1]],
    ]


def subdivide_triangle(
        strategy, iterations=8, width=1080, height=1080, background_color=Colors.white,
        line_color=Colors.black, resize_size=None
):
    triangle = [
        (width / 2, 0),  # vertex A
        (0, height),  # vertex B
        (width, height),  # vertex C
    ]

    image, draw = new_image(size=(width, height), color=background_color)

    previous_generation_triangles = [triangle]  # start with a list that consist of the starting triangle only
    for iteration in range(iterations):
        new_triangles = []
        for triangle in previous_generation_triangles:
            # for each polygon in the previous generation, subdivide that polygon into two new polygons,
            # extend the list of new triangles with the two subdivided triangles
            new_triangles += divide(triangle_vertices=triangle, iteration=iteration, strategy=strategy)

        # override the previous triangles with the new one, we only need to remember the last iteration
        previous_generation_triangles = new_triangles

    # previous_generation_triangles contains all triangles calculated in the last iteration, draw all of them!
    for triangle in previous_generation_triangles:
        draw.polygon(xy=triangle, outline=line_color)

    save_image(image=image, file_name='Subdivide_i{}_{}'.format(iterations, strategy), resize_size=resize_size)


def recursively_subdivide_triangle(strategy, total_iterations=8, width=1080, height=1080, resize_size=None):
    """
    Generates the same output as the methods above, but all the logic compressed to a few lines,
    and it seems to be slightly faster.
    """
    def subdivide_and_draw(draw, vertices, i):
        if i < total_iterations:
            subdivide_vertex = vertices.pop(strategy[i % len(strategy)])
            midpoint = ((vertices[0][0] + vertices[1][0]) / 2, (vertices[0][1] + vertices[1][1]) / 2)
            for vertex_index in range(2):
                subdivide_and_draw(draw, vertices=[subdivide_vertex, midpoint, vertices[vertex_index]], i=i + 1)
        else:
            draw.polygon(xy=vertices)

    image, draw = new_image(size=(width, height))
    subdivide_and_draw(draw=draw, vertices=[(width / 2, 0), (0, height), (width, height)], i=0)
    save_image(image=image, file_name='Subdivide_i{}_{}'.format(total_iterations, strategy), resize_size=resize_size)


subdivide_triangle(strategy=[0, 2, 1], iterations=15, width=1080 * 3, height=1080 * 3, resize_size=(1080, 1080))
