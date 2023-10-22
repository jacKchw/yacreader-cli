#!/usr/bin/env python3

from pathlib import Path
import argparse
import shutil


def main():
    # get dir path
    parser = argparse.ArgumentParser(description="zip all sub directory as cbz")
    parser.add_argument("dir", help="base directory")
    args = parser.parse_args()
    dirPath = Path(args.dir)

    for dirPath in dirPath.iterdir():
        if not dirPath.is_dir():
            continue

        # zip
        shutil.make_archive(dirPath, "zip", dirPath)
        shutil.move(str(dirPath.absolute()) + ".zip", str(dirPath.absolute()) + ".cbz")


if __name__ == "__main__":
    main()
