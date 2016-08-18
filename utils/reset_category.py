#!/usr/bin/env python3

if __name__ == '__main__' and __package__ is None:
    import os
    # __file__ should be defined in this case
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.append(PARENT_DIR)

from utils import DatabaseDAO
import sys

if len(sys.argv) != 2:
    print("1 Arguments, in this order: title")
    sys.exit()

article = dict()
article["title"] = sys.argv[1]

DatabaseDAO.reset_category(article)
