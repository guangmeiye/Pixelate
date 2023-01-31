import logging
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
from functools import cached_property
from typing import Array

from cli_command_parser import Command, Positional, main
from cli_command_parser import Positional, Flag

log = logging.getLogger(__name__)


LEGO_COLORS = Path('data\colors.csv')
BRICK_PATH = Path('data\bricks\1x1.png')


class pixelate(Command):
    image_path = Positional(nargs='*', type=Path, help='Paths for image files or directories containing music files.')
    color = Flag('-C', type=Path , help='Turn the image to black and white.', default=BRICK_PATH)

    def main(self):
        rgb_range = list(LegoColorBrick().rgb_range)
        img = self.convert_image_rgb(rgb_range)
        return self.matrix_to_image(img)

    def load_image(self) ->Image:
        img = Image.open(self.image_path)
        img = img.convert("RGB")
        return img

    @cached_property
    def image(self) ->Image:
        return self.load_image(self.image_path)

    @cached_property
    def rgb_matrix(self):
        return np.array(self.image)

    def matrix_to_image(self, rgb_matrix: Array) ->Image:
        return Image.fromarray(rgb_matrix)

    def closest_color(self, color, rgb_range):
        rgb_range = np.array(rgb_range)
        color = np.array(color)
        distances = np.sqrt(np.sum((rgb_range-color)**2,axis=1))
        index_of_smallest = np.where(distances==np.amin(distances))
        smallest_distance = rgb_range[index_of_smallest]
        return smallest_distance 

    def convert_image_rgb(self, rgb_range):
        rgb_matrix = self.rgb_matrix.copy()
        for i, row in enumerate(rgb_matrix):
            for j, item in enumerate(row):
                rgb_matrix[i][j] = self.closest_color(item, rgb_range)
        return rgb_matrix

    #the covert level should be adjustable


    #convert 1x1 bricks to the color we want
    def convert_brick_color(self, convert_color: tuple[int, int, int]) ->Image:
        img = self.load_image(self.brick_path)
        data = img.getdata()
        new_image_data = []
        for item in data:
            if item[0] in list(range(190, 256)):
                new_image_data.append(convert_color)
            else:
                new_image_data.append(item)
        img.putdata(new_image_data)
        return img
    # resize the image based on given size
    # base plate size: 16*32, 32*32, 24 * 24

    #generate new lego picture by bricks


# convert lego color csv to a dictionary and store the results
class ColorBrick:
    __slot__ = ('id', 'name', 'hex', 'rgb', 'is_trans')

    id :int
    name: str
    hex: str
    rgb: tuple[int, int, int]
    is_trans: str

    def __init__(self, id, name, rgb, is_trans, hex):
        self.id = id
        self.name = name
        self.hex = hex
        self.rgb = rgb
        self.is_trans = is_trans

class LegoColorBrick:
    def lego_colors(self):
        return pd.read_csv('/content/colors.csv')

    def hex_to_rgb(self, hex):
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)) 

    @cached_property
    def lego_colors(self):
        # a list of ColorBrick
        lego_colors = {}
        for index, row in self.lego_colors.iterrows():
            rgb = self.hex_to_rgb(row['hex'])
            lego_colors[rgb] = ColorBrick(index, row['name'], rgb, row['hex'], row['is_trans'])
        return lego_colors

    def rgb_range(self):
        # get a range of rgb color
        pass


if __name__ == '__main__':
    main()