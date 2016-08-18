#!/usr/bin/env python3

if __name__ == '__main__' and __package__ is None:
    import os
    # __file__ should be defined in this case
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.append(PARENT_DIR)

from utils import DatabaseDAO
import sys

full = len(sys.argv) == 2 and sys.argv[1] == "full"


def main():
    categories = DatabaseDAO.get_categories()
    categories = {str(int(x["identity"])): x["name"] for x in categories}
    cnt = 0
    for article in DatabaseDAO.get_interesting():
        print(str(cnt) + " -- " + article["title"] + " ")
        print()
        print("Categories: " + ",".join([categories[str(i)] for i in article["category"]]))
        print()
        if full:
            print(article["abstract"])
            print()

        cnt += 1


if __name__ == "__main__":
    main()
