#!/usr/bin/env python3
# crop any image

from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color
import argparse
from pathlib import Path


def main():
    # get args
    parser = argparse.ArgumentParser(description="crop any image")
    parser.add_argument("-i", "--input", required=True, help="input file")
    parser.add_argument("-l", "--left", type=int, required=True, help="left position")
    parser.add_argument("-r", "--right", type=int, help="right position")
    parser.add_argument(
        "-d",
        "--display",
        action="store_true",
        help="show preview and ask for confirm",
    )
    args = parser.parse_args()
    inputFilePath = Path(args.input)

    left = args.left
    right = args.right

    with Image(filename=inputFilePath) as img:
        (w, h) = img.size

        if not right:
            # use default ratio
            right = round(0.7 * h + left)

        if args.display:
            # show preview
            print("left: ", left)
            print("right: ", right)
            with Drawing() as draw:
                draw.stroke_width = (right - left) * 0.005
                draw.stroke_color = Color("red")
                draw.fill_opacity = 0
                points = [(left, 0), (right, 0), (right, h), (left, h)]
                draw.polygon(points)
                with img.clone() as i:
                    draw(i)
                    display(i)

            confirm = input("Confirm? [Y]/N")
            if confirm == "N" or confirm == "n":
                exit()

        # crop image
        with img.clone() as i:
            i.crop(left=left, top=0, right=right)
            i.save(filename=inputFilePath)


if __name__ == "__main__":
    main()
