#!/usr/bin/env python3

import DatabaseDAO
import sys

if len(sys.argv) < 3:
    print("Need 2 arguments, title and interest")
    sys.exit(0)

title = sys.argv[1].lower()
interest = float(sys.argv[2])

DatabaseDAO.update_article(title, interest)
