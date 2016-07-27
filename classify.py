
from utils import DatabaseDAO

CATEGORIES = []


def setup():
    categories = [category["name"] for category in DatabaseDAO.get_categories()]
    for cat in CATEGORIES:
        if cat not in categories:
            DatabaseDAO.insert_category(cat)


def clear():
    print(chr(27) + "[2J")


def print_categories():
    categories = [(entry["identity"],  entry["name"]) for entry in DatabaseDAO.get_categories()]
    print("-" * 20)
    print("Number: Category")
    print("-" * 20)
    print()
    for entry in sorted(categories, key=lambda tup: tup[0]):
        print(str(entry[0]) + " : " + str(entry[1]))
    print()
    print("-" * 20)
    print()


def main():
    setup()
    category_ids = set([category["identity"] for category in DatabaseDAO.get_categories()])
    for article in DatabaseDAO.get_interesting():
        if "category" not in article:
            clear()
            print_categories()
            print(article["title"])
            print()
            print("Interest: " + str(article["interest"]))
            print()
            print(article["abstract"])
            print()
            acceptable = False
            while acceptable is False:
                cats = input("Categories (seperate by comma for multiple)? ")
                if cats == "q":
                    return
                buckets = set([int(x.strip()) for x in cats.split(",")])
                if buckets <= category_ids:
                    acceptable = True
                else:
                    print("One of those is not a valid category")
            DatabaseDAO.categorize_article(article, ",".join([str(x) for x in buckets]))


if __name__ == "__main__":
    main()
