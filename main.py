#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np
import argparse

def mercator_to_equirectangular(image):
    width, height = image.size
    equirectangular = Image.new("RGBA", (width, int(height / 2)))

    for x in range(width):
        for y in range(height // 2):
            lat = np.pi * (y / (height / 2) - 0.5)
            lon = 2 * np.pi * x / width - np.pi
            x_mercator = (lon / np.pi + 1) * width / 2
            y_mercator = height / 2 - np.log(np.tan(np.pi / 4 + lat / 2)) * height / (2 * np.pi)
            if x_mercator >= 0 and x_mercator < width and y_mercator >= 0 and y_mercator < height:
                equirectangular.putpixel((x, y), image.getpixel((int(x_mercator), int(y_mercator))))

    return equirectangular

def equirectangular_to_mercator(image):
    width, height = image.size
    mercator = Image.new("RGBA", (width, height * 2))

    for x in range(width):
        for y in range(height * 2):
            lon = np.pi * (2 * x / width - 1)
            lat = np.arctan(np.sinh(np.pi * (1 - 2 * y / (height * 2))))
            x_equirectangular = int((lon + np.pi) * width / (2 * np.pi))
            y_equirectangular = int((lat + np.pi / 2) * height / np.pi)
            if x_equirectangular >= 0 and x_equirectangular < width and y_equirectangular >= 0 and y_equirectangular < height:
                mercator.putpixel((x, y), image.getpixel((x_equirectangular, y_equirectangular)))

    return mercator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='main.py', description="Convert mercator to equirectangular projected images and vice versa.")
    parser.add_argument('-i', '--invert', action='store_true', help="convert equirectangular to mercator")
    parser.add_argument('input_image', type=argparse.FileType('r'), help="the input image")
    parser.add_argument('output_image', type=argparse.FileType('w'), help="the output image")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    image = Image.open(args.input_image.name)

    if args.invert:
      result = mercator_to_equirectangular(image)
    else:
      result = equirectangular_to_mercator(image)

    result = result.rotate(180)
    result = result.transpose(Image.FLIP_LEFT_RIGHT)
    result.save(args.output_image.name)