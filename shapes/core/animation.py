import glob
import os
import shutil
import subprocess

from settings import (
    BITRATE, FRAMES_PER_SECOND, IMAGE_EXTENSION, IMAGE_DIRECTORY_NAME,
    VIDEO_CODEC, VIDEO_EXTENSION, VIDEO_PIXEL_FORMAT,
)
from shapes.core.image import get_datetime_string


def make_movie(name=None):
    """
    Take all files with extension <IMAGE_EXTENSION> that are in the settings.IMAGE_DIRECTORY_NAME,
    and put them together in a mp4 file (or .mov, depending on the value in VIDEO_EXTENSION).
    Replace all those files to a subdirectory.

    For example, when the settings.IMAGE_DIRECTORY_NAME is called 'files', the IMAGE_EXTENSION is 'jpeg'
    and the VIDEO_EXTENSION is 'mp4':

    BEFORE (a bunch of 'jpeg' files in the 'files' directory):

    files
    ├── image_1.jpeg
    ├── image_2.jpeg
    ├── image_3.jpeg
    └── image_4.jpeg

    AFTER (a subdirectory is made, containing the mp4 file, and a 'stills' directory contains all original jpegs):

    files
    └── <time_stamp>_movie
        ├── <time_stamp>_movie.mp4
        └── stills
            ├── image_1.jpeg
            ├── image_2.jpeg
            ├── image_3.jpeg
            └── image_4.jpeg
    """
    #
    # Create the movie file and place it in the same directory as the images
    #
    file_name = '{}_{}_movie'.format(get_datetime_string(), name or '')

    image_source_pattern = os.path.join(IMAGE_DIRECTORY_NAME, '*.{}'.format(IMAGE_EXTENSION))
    output_video_file_path = os.path.join(IMAGE_DIRECTORY_NAME, '{}.{}'.format(file_name, VIDEO_EXTENSION))

    bitrate_part = '-b:v {}k -bufsize {}k'.format(BITRATE, BITRATE)
    ffmpeg_command = "ffmpeg -framerate {} -pattern_type glob -i '{}' {} -c:v {} -pix_fmt {} {}".format(
        FRAMES_PER_SECOND, image_source_pattern, bitrate_part, VIDEO_CODEC, VIDEO_PIXEL_FORMAT, output_video_file_path)

    proc = subprocess.Popen(ffmpeg_command, shell=True)
    proc.wait()

    #
    # Create sub directories, and replace the movie file and the still images to this subdirectory
    #
    video_destination_dir = os.path.join(IMAGE_DIRECTORY_NAME, file_name)
    os.mkdir(video_destination_dir)
    shutil.move(output_video_file_path, video_destination_dir)

    # move every image to the 'stills' directory
    stills_dir = os.path.join(video_destination_dir, 'stills')
    os.mkdir(stills_dir)
    image_file_paths = glob.glob(image_source_pattern)
    for image_file_path in image_file_paths:
        shutil.move(image_file_path, stills_dir)
