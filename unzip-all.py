#!/usr/bin/env python3

from pathlib import Path
import argparse
import shutil
from os import makedirs


def main():
    # get dir path
    parser = argparse.ArgumentParser(
        description="unzip all zip/cbz files in the directory"
    )
    parser.add_argument("dir", help="directory of zip/cbz files")
    args = parser.parse_args()
    dirPath = Path(args.dir)

    for file in dirPath.iterdir():
        if file.suffix != ".zip" and file.suffix != ".cbz":
            continue
        if not file.is_file():
            continue

        # check if dir exist
        unzipDir = file.parent / file.stem
        if unzipDir.exists():
            print("skipped ", unzipDir.name, " because it already exists")
            continue

        # unzip
        makedirs(unzipDir)
        shutil.unpack_archive(file, unzipDir, "zip")


if __name__ == "__main__":
    main()
