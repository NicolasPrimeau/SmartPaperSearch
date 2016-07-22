#!/usr/bin/env python3

if __name__ == '__main__' and __package__ is None:
    import os
    # __file__ should be defined in this case
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.append(PARENT_DIR)

from utils import DatabaseDAO

import sys

if len(sys.argv) < 3:
    print("Need 2 arguments, title and interest")
    sys.exit(0)

title = sys.argv[1].lower()
interest = float(sys.argv[2])

DatabaseDAO.update_article(title, interest)
