#!/usr/bin/env python3

from wand.image import Image
from wand.display import display
import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path


def main():
    # get args
    parser = argparse.ArgumentParser(description="select page as thumbnail")
    parser.add_argument("-i", "--input", required=True, help="input file")
    parser.add_argument(
        "-p", "--page", type=int, required=True, help="page number to be thumbnail"
    )
    parser.add_argument(
        "-d",
        "--display",
        action="store_true",
        help="display preview and ask for confirm",
    )
    args = parser.parse_args()
    inputFilePath = Path(args.input)

    with tempfile.TemporaryDirectory() as tempDir:
        unzipDirPath = Path(tempDir)
        # unzip file
        shutil.unpack_archive(inputFilePath, unzipDirPath, "zip")

        # get first fileName
        files = [f for f in unzipDirPath.iterdir() if f.is_file()]
        if len(files) < args.page:
            raise ValueError("selected page doesn't exist")
        files.sort()
        imageFileName = files[args.page]

        newImageFilePath = imageFileName.parent / ("_0" + imageFileName.suffix)
        if newImageFilePath.exists():
            raise FileExistsError(newImageFilePath.name + " exist.")

        if args.display:
            with Image(filename=imageFileName) as img:
                display(img)
            confirm = input("Confirm? [Y]/N")
            if confirm == "N" or confirm == "n":
                return

        # zip file
        with zipfile.ZipFile(inputFilePath, "w") as zf:
            zf.write(imageFileName, arcname=newImageFilePath.name)
            for file in files:
                zf.write(file, arcname=file.name)


if __name__ == "__main__":
    main()
