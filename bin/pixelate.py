import logging
from PIL import Image
from pathlib import Path
from functools import cached_property
import numpy as np

from ds_tools.argparsing import ArgParser
from ds_tools.core.main import wrap_main
from cli_command_parser import Positional, Flag

log = logging.getLogger(__name__)


LEGO_COLORS = Path('data\colors.csv')


def parser():
    # fmt: off
    parser = ArgParser(description='Pixelate')
    path = Positional(nargs='*', type=Path, help='Paths for image files or directories containing music files.')
    color = Flag('-C', help='Turn the image to black and white.')
    # fmt: on
    return parser

class pixelate:
    def __init__(self, image_path: Path) -> None:
        self.image_path = image_path

    @cached_property
    def image(self) ->Image:
        img = Image.open(self.image_path)
        img = img.convert("RGB")
        return img

    @cached_property
    def rgb_matrix(self):
        return np.array(self.image)

    def matrix_to_image(self, rgb_matrix: Array) ->Image:
        return Image.fromarray(rgb_matrix)
    #convert the array to the rgb range we have
    #the covert level should be adjustable


    #convert 1x1 bricks to the color we want


    # resize the image based on given size


    #generate new lego picture by bricks


# convert lego color csv to a dictionary and store the results
class ColorBrick:
    __slot__ = ('id', 'name', 'hex', 'rgb', 'type')

    id :int
    name: str
    hex: str
    rgb: tuple[int, int, int]
    type: str

    def __init__(self, id, name, hex, rgb, type):
        self.id = id
        self.name = name
        self.hex = hex
        self.rgb = rgb
        self.type = type

class LegoColorBricks:

    def load_color_csv(self):
        pass

    def hex_to_rgb(self, hex):
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)) 

    def lego_colors(self):
        # a list of ColorBrick
        pass

    def rgb_range(self):
        # get a range of rgb color
        pass

@wrap_main
def main():
    args = parser().parse_args()


if __name__ == '__main__':
    main()