#!/usr/bin/env python3

from wand.image import Image
import argparse
import shutil
import tempfile
from math import floor
from pathlib import Path
import zipfile


def main():
    # get args
    parser = argparse.ArgumentParser(description="crop images left or right")
    parser.add_argument("-i", "--input", required=True, help="input file")
    parser.add_argument(
        "-r",
        "--right",
        action="store_true",
        help="crop the right side of the thumbnail",
    )
    args = parser.parse_args()
    inputFilePath = Path(args.input)

    with tempfile.TemporaryDirectory() as tempDir:
        unzipDirPath = Path(tempDir)
        # unzip file
        shutil.unpack_archive(inputFilePath, unzipDirPath, "zip")

        # get first fileName
        files = [f for f in unzipDirPath.iterdir() if f.is_file()]
        files.sort()
        prevImagePath = Path(files[0])

        newImageFilePath = prevImagePath.parent / ("_0" + prevImagePath.suffix)
        if newImageFilePath.exists():
            raise FileExistsError(newImageFilePath.name + " exist.")

        # crop thumbnail
        with Image(filename=prevImagePath) as img:
            (w, _) = img.size
            with img.clone() as i:
                newW = floor(w / 2)
                if args.right:
                    i.crop(newW, 0, width=newW)
                else:
                    i.crop(0, 0, right=newW)
                i.save(filename=newImageFilePath)
        files.append(newImageFilePath)

        # zip file
        with zipfile.ZipFile(inputFilePath, "w") as zf:
            for file in files:
                zf.write(file, arcname=file.name)


if __name__ == "__main__":
    main()
