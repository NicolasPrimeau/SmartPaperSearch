#!/usr/bin/env python3

if __name__ == '__main__' and __package__ is None:
    import os
    # __file__ should be defined in this case
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.append(PARENT_DIR)

from utils import DatabaseDAO
import sys

if len(sys.argv) != 4 and len(sys.argv) != 2:
    print("3 Arguments, in this order: title, interest, abstract, or give the path to a properly formatted file")
    sys.exit()

if len(sys.argv) == 4:
    title = sys.argv[1].lower()
    interest = int(sys.argv[2])
    abstract = sys.argv[3]
else:
    lines = [line.strip() for line in open(sys.argv[1])]
    buffer = list()
    title = None
    interest = 1
    abstract = None
    for line in lines:
        if line is not None and line != "":
            buffer.append(line)
        elif title is None:
                title = " ".join(buffer)
                buffer.clear()
    if abstract is None:
        abstract = " ".join(buffer)
        buffer.clear()
    del buffer

if interest not in (0, 1):
    print("Interest must be 0 or 1")
    sys.exit()

DatabaseDAO.save_article_full(title, abstract, interest)
