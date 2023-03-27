import logging
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from pathlib import Path
from functools import cached_property


log = logging.getLogger(__name__)


LEGO_COLORS = Path('data\colors.csv')


class Pixelate:
    def __init__(self, image_path: Path, brick_size: int, colors: int) -> None:
        self.image_path = image_path
        self.brick_size = brick_size
        self.colors = colors

    def main(self):
        rgb_range = list(LegoColorBrick().rgb_range)
        img = self.convert_image_rgb(rgb_range)
        return self.matrix_to_image(img)

    def load_image(self, image_path) ->Image:
        img = Image.open(image_path)
        img = img.convert("RGB")
        return img

    @cached_property
    def image(self) ->Image:
        return self.load_image(self.image_path)

    @cached_property
    def rgb_matrix(self):
        return np.array(self.image)

    def matrix_to_image(self, rgb_matrix) ->Image:
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
    def render(self):
        num_rows, num_cols = len(self.rgb_matrix), len(self.rgb_matrix[0])
        image_width, image_height = num_cols * self.brick_size, num_rows * self.brick_size
        image = Image.new('RGB', (image_width, image_height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for row in range(num_rows):
            for col in range(num_cols):
                brick_color = self.rgb_matrix[row][col]
                # Todo: add default rbg_range dicts based on the colors paser
                rgb_range = LegoColorBrick().rgb_range
                brick_color = self.closest_color(brick_color, rgb_range)
                brick_x1, brick_y1 = col * self.brick_size, row * self.brick_size
                brick_x2, brick_y2 = brick_x1 + self.brick_size, brick_y1 + self.brick_size
                draw.rectangle((brick_x1, brick_y1, brick_x2, brick_y2), fill=brick_color)
        return image

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
    def resize_image(self, size):
        with Image.open(self.image_path) as img:
            img = img.resize(size)
        return img

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

    @cached_property
    def rgb_range(self):
        # get a range of rgb color
        print(self.lego_colors)
        return list(self.lego_colors)
