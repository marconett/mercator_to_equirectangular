#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np
import argparse

def mercator_to_equirectangular(image):
    width, height = image.size
    equirectangular = Image.new("RGB", (width, int(height / 2)))
    for x in range(width):
        for y in range(height // 2):
            lat = np.pi * (y / (height / 2) - 0.5)
            lon = 2 * np.pi * x / width - np.pi
            x_mercator = (lon / np.pi + 1) * width / 2
            y_mercator = height / 2 - np.log(np.tan(np.pi / 4 + lat / 2)) * height / (2 * np.pi)
            if x_mercator >= 0 and x_mercator < width and y_mercator >= 0 and y_mercator < height:
                equirectangular.putpixel((x, y), image.getpixel((int(x_mercator), int(y_mercator))))
    return equirectangular

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='mercator_to_equirectangular.py', description="Input a mercator projected image and output a equirectangular projected image.")
    parser.add_argument('input_image', type=argparse.FileType('r'), help="the mercator image")
    parser.add_argument('output_image', type=argparse.FileType('w'), help="the equirectangular image")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    image = Image.open(args.input_image.name)
    equirectangular = mercator_to_equirectangular(image)
    equirectangular = equirectangular.rotate(180)
    equirectangular = equirectangular.transpose(Image.FLIP_LEFT_RIGHT)
    equirectangular.save(args.output_image.name)