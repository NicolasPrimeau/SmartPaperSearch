#!/usr/bin/env python3

if __name__ == '__main__' and __package__ is None:
    import os
    # __file__ should be defined in this case
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.append(PARENT_DIR)

from utils import DatabaseDAO
import sys

if len(sys.argv) != 4:
    print("3 Arguments, in this order: title, interest, abstract")
    sys.exit()

title = sys.argv[1].lower()
interest = int(sys.argv[2])
abstract = sys.argv[3]

if interest not in (0, 1):
    print("Interest must be 0 or 1")
    sys.exit()

DatabaseDAO.save_article_full(title, abstract, interest)
