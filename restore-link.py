#!/usr/bin/env python3
# use sqlite record to recreate symlink 
# e.g. ./restore-link.py -i /home/jack/Documents/ecrypt-lib
import sqlite3
import argparse
from pathlib import Path
from os import path


def main():
    # get input file path
    parser = argparse.ArgumentParser(description="update library metadata")
    parser.add_argument("-i", "--input", required=True, help="path of library")
    args = parser.parse_args()

    input = Path(args.input)
    sqlPath = input / '.yacreaderlibrary' / 'library.ydb'

    # establish connection
    con = sqlite3.connect(sqlPath)
    cur = con.cursor()

    # get creator or series from path
    res = cur.execute("SELECT * FROM comic;")
    comics = res.fetchall()
    for comic in comics:

        comicInfoId = comic[2]
        filePath = input / Path(comic[4][1:])
        items = filePath.parts
        dir = items[-3]
        value = items[-2]

        if dir == "creator":
            continue

        query = "SELECT * FROM comic WHERE comicInfoId = ? ORDER BY path LIMIT 1;"

        creatorRes = cur.execute(query, (comicInfoId,))
        creatorComic = creatorRes.fetchone()
        creatorPath =  input / Path(creatorComic[4][1:])
        print(filePath)
        filePath.parent.mkdir(parents=True, exist_ok=True)
        filePath.symlink_to(path.relpath(creatorPath, filePath.parent))
    

    # commit changes
    cur.close()


if __name__ == "__main__":
    main()
