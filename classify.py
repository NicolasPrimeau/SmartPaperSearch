import os

import yaml

from utils import DatabaseDAO

resources_file = 'resources/config/resources.yml'

if os.path.isfile(resources_file):
    with open(resources_file) as f:
        try:
            CATEGORIES = yaml.load(f)["categories"]
        except KeyError:
            print("Category file is not correct")

else:
    raise ValueError("Need categories file")


def setup():
    categories = [category["name"] for category in DatabaseDAO.get_categories()]
    for cat in categories:
        if cat not in categories:
            DatabaseDAO.insert_category(cat)


def clear():
    print(chr(27) + "[2J")


def print_categories():
    categories = [(entry["identity"],  entry["name"]) for entry in DatabaseDAO.get_categories()]
    print("-" * 20)
    print("Number: Category")
    print("-" * 20)
    for entry in sorted(categories, key=lambda tup: tup[0]):
        print(str(int(entry[0])) + " : " + str(entry[1]))
    print("-" * 20)
    print()


def main():
    setup()
    category_ids = set([category["identity"] for category in DatabaseDAO.get_categories()])
    for article in DatabaseDAO.get_interesting():
        if "category" not in article or len(article["category"]) == 0:
            clear()
            print_categories()
            print(article["title"])
            print()
            print(article["abstract"])
            print()
            acceptable = False
            while acceptable is False:
                cats = input("Categories (seperate by comma for multiple)? ")
                if cats == "q":
                    return
                elif cats == "d":
                    DatabaseDAO.update_article(article["title"], 0)
                    break
                buckets = set([int(x.strip()) for x in cats.split(",")])
                if buckets <= category_ids:
                    DatabaseDAO.categorize_article(article, [str(x) for x in buckets])
                    acceptable = True
                else:
                    print("One of those is not a valid category")

if __name__ == "__main__":
    main()
