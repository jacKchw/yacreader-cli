#!/usr/bin/env python3
import sqlite3
import argparse
from pathlib import Path


def main():
    # get input file path
    parser = argparse.ArgumentParser(description="update library metadata")
    parser.add_argument("-i", "--input", required=True, help="path of library.ydb")
    args = parser.parse_args()

    con = sqlite3.connect(args.input)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM comic;")
    comics = res.fetchall()
    for comic in comics:
        comicInfoId = comic[2]

        # get creator or series
        filePath = Path(comic[4])
        items = filePath.parts
        query = ""
        dir = items[-3]
        value = items[-2]
        print(dir, value)
        if dir == "creator":
            query = "UPDATE comic_info SET writer = ? WHERE id = ?;"
        if dir == "series":
            query = "UPDATE comic_info SET series = ? WHERE id = ?;"
        if dir == "tags" or query == "":
            continue

        cur.execute(query, (value, comicInfoId))

    res = cur.execute("SELECT DISTINCT comicInfoId, fileName FROM comic;")
    comics = res.fetchall()
    for comic in comics:
        # get title
        comicInfoId = comic[0]
        fileName = Path(comic[1])
        title = fileName.stem
        cur.execute(
            "UPDATE comic_info SET title = ? WHERE id = ?;", (title, comicInfoId)
        )

    cur.execute("UPDATE comic_info SET type = 1 WHERE type <> 1;")

    con.commit()
    cur.close()

    return


if __name__ == "__main__":
    main()
