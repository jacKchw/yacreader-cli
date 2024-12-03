#!/usr/bin/env python3
import sqlite3
import argparse
from pathlib import Path


def main():
    # get input file path
    parser = argparse.ArgumentParser(description="update library metadata")
    parser.add_argument("-i", "--input", required=True, help="path of library.ydb")
    parser.add_argument("-v", "--verbose", required=False, help="explain what is being done", action= argparse.BooleanOptionalAction)
    args = parser.parse_args()
    isVerbose = args.verbose == True


    # establish connection
    con = sqlite3.connect(args.input)
    con.row_factory = sqlite3.Row
    cur = con.cursor()


    res = cur.execute("SELECT * FROM comic_info;")
    comicInfos = res.fetchall()
    for comicInfo in comicInfos:
        comicInfoId = comicInfo["id"]
    
        # get creator, series and tags from path
        res = cur.execute("SELECT * FROM comic WHERE comicInfoId = ?;", (comicInfoId,))
        comics = res.fetchall()


        title = ""
        infoColumn = {
        "creator" : "writer",
        "series" : "series",
        "tags" : "synopsis"
        }
        infoValue = {
        "creator" : [],
        "series" : [],
        "tags" : []
        }

        for comic in comics:
            if comic["path"] is None:
                continue
            filePath = Path(comic["path"])
            if filePath.stem != "_":
                title = filePath.stem

            items = filePath.parts
            dir = items[-3]
            value = items[-2]

            if dir not in infoValue.keys():
                continue

            infoValue[dir].append(value)


        # get title
        
        if title != "" and title != comicInfo["title"]:
            cur.execute(
                "UPDATE comic_info SET title = ?  WHERE id = ?;", (title, comicInfoId)
            )
            if isVerbose:
                print("Updated title:", title)

        
        # update creator, series and tags in comic_info
        for key in infoValue:
            infos = infoValue[key]
            columnName =infoColumn[key]

            if len(infos) >0:
                infosStr = " / ".join(infos)
                if comicInfo[columnName] == infosStr:
                    continue
                cur.execute("UPDATE comic_info SET %s = ? WHERE id = ?;"%columnName,( infosStr, comicInfoId))
                if isVerbose:
                    print("Updated ",columnName +":", title, '"'+infosStr+'"')


    # change type to manga
    cur.execute("UPDATE comic_info SET type = 1 WHERE type <> 1;")

    # commit changes
    con.commit()
    cur.close()


if __name__ == "__main__":
    main()
