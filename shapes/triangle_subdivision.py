from shapes.core.image import new_image, save_image


def code_golf(iterations=12, width=1080, height=1080):
    image, draw = new_image(size=(width, height))

    polygons = [[(width, 0), (width, height), (0, 0)], [(0, height), (width, height), (0, 0)]]
    for i in range(iterations):
        polygons = [item for sublist in [[
            [poly[i % 3], poly[(i + k) % 3], ((poly[(i + 1) % 3][0] + poly[(i + 2) % 3][0]) / 2,
                                              (poly[(i + 1) % 3][1] + poly[(i + 2) % 3][1]) / 2)] for k in range(1, 3)
        ] for poly in polygons] for item in sublist]

    for polygon_points in polygons:  # only draw the polygons added in the last iteration
        draw.polygon(xy=polygon_points)

    save_image(image=image, file_name='triangle_subdivide_i{}'.format(iterations))
