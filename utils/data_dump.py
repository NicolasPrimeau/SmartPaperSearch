#!/usr/bin/env python3

import DatabaseDAO


def main():
    cnt = 0
    for article in DatabaseDAO.get_interesting():
        print(str(cnt) + " -- " + article["title"])
        print()
        cnt += 1


if __name__ == "__main__":
    main()