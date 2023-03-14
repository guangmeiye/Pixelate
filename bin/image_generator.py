import logging
from pathlib import Path
from PIL import Image
from pixelate import Pixelate

from cli_command_parser import Command, Positional, main
from cli_command_parser import Positional, Flag

log = logging.getLogger(__name__)

BRICK_PATH = Path('data\bricks\1x1.png')


class LegoImageGenerator(Command):
    """
    Generates a Lego-style image from an input image file.
    """
    image_path = Positional(nargs='*', type=Path, help='Paths for image files or directories containing music files.')
    brick_size = Positional('-b', type=int , help='The size of each Lego brick in pixels', default=16)
    colors = Positional('-c', type=int , help='The number of colors to use in the output image', default=6)

    def generate_lego_image(self, input_path, output_path):
        """
        Generates a Lego-style image from an input image file and saves it to a file.
        :param input_path: The path to the input image file.
        :param output_path: The path to save the output Lego-style image file.
        """
        with Image.open(input_path) as img:
            legoizer = Pixelate(img, self.brick_size, self.colors)
            lego_image = legoizer.render()

        lego_image.save(output_path)