#!/usr/bin/env python3

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    # __file__ should be defined in this case
    PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(PARENT_DIR)

from utils import DatabaseDAO


def main():
    cnt = 0
    for article in DatabaseDAO.get_interesting():
        print(str(cnt) + " -- " + article["title"])
        print()
        cnt += 1


if __name__ == "__main__":
    main()
