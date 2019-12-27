import os
from PIL import Image, ImageDraw
from datetime import datetime

from settings import (
    BACKGROUND_COLOR, DATETIME_FORMAT, DEFAULT_IMAGE_SIZE,
    IMAGE_DIRECTORY_NAME, IMAGE_EXTENSION, IMAGE_FORMAT, IMAGE_FORMAT_COLOR_MODE,
)


# if you get a DecompressionBombError, you can uncomment the line below, and no check on max pixels will be made.
# Only do this if you trust the image file (so when you created it yourself)
# This is a safety check, that prevents systems for opening very large (and possible corrupt) image files.
# Of course, when the file is very large, your computer might not be able to process it and the program will be killed.
# Image.MAX_IMAGE_PIXELS = None


def get_datetime_string():
    """
    All file names should start with a date string, so they are unique and in
    both alphabetical and chronological order.
    """
    return datetime.now().strftime(DATETIME_FORMAT)


def new_image(size=DEFAULT_IMAGE_SIZE, color=BACKGROUND_COLOR):
    image = Image.new(mode=IMAGE_FORMAT_COLOR_MODE, size=size, color=color)
    draw = ImageDraw.Draw(image)

    return image, draw


def save_image(image, file_name, resize_size=None):
    """
    :param image: Pil.Image instance
    :param file_name: description that will be included in the actual filename
    :param resize_size: when you wish to resize the image, provide the size as a tuple of two integers, like (500, 500)
    :return: the file_path of the created image
    """
    # the part of the file name before the extension, make sure it will never be longer then 250 characters
    file_name = '{}_{}'.format(get_datetime_string(), file_name)[:250]
    file_name_with_extension = '{}.{}'.format(file_name, IMAGE_EXTENSION)
    new_image_path = os.path.join(IMAGE_DIRECTORY_NAME, file_name_with_extension)

    if resize_size is not None:
        image = image.resize(size=resize_size, resample=Image.ANTIALIAS)   # ALWAYS preserves aspect ratio

    image.save(fp=new_image_path, format=IMAGE_FORMAT)

    print('Saved {}'.format(new_image_path))
    return new_image_path
