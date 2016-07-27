from pymongo import MongoClient

DB_NAME = "MendeleyAutoScrape"
REVIEWED = "articles"
CATEGORIES = "categories"


def get_categories(db_name=DB_NAME):
    with MongoClient() as client:
        return list(client[db_name][CATEGORIES].find())


def insert_category(name, db_name=DB_NAME):
    with MongoClient() as client:
        ident = client[db_name][CATEGORIES].count()
        if client[db_name][CATEGORIES].find_one({"identity": ident}) is not None:
            print("Category Database Corrupted, non unique ids! Please Fix!")
            return
        elif client[db_name][CATEGORIES].find_one({"name": name}) is not None:
            print("Can not add identical category")
            return
        client[db_name][CATEGORIES].insert_one({
            "name": name,
            "identity": ident
        })


def categorize_article(article, categories, db_name=DB_NAME):
    if isinstance(categories, list):
        categories = ",".join(categories)

    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": article.title.strip()
            }, {"$set": {
                "title": article.title.strip(),
                "category": categories
            }})


def save_article(article, interest, db_name=DB_NAME):
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": article.title.strip()
            }, {"$set": {
                "title": article.title.strip(),
                "abstract": article.abstract,
                "interest": interest
            }}, upsert=True)


def save_article_full(title, abstract, interest, db_name=DB_NAME):
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": title.strip()
            }, {"$set": {
                "title": title.strip(),
                "abstract": abstract,
                "interest": interest
            }}, upsert=True)


def update_article(title, interest, db_name=DB_NAME):
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": title.strip()
            }, {"$set": {
                "interest": interest
            }})


def get_interesting(db_name=DB_NAME):
    with MongoClient() as client:
        return list(client[db_name][REVIEWED].find({"interest": 1}))


def contains(article, db_name=DB_NAME):
    return get_article(article, db_name=db_name) is not None


def get_articles(db_name=DB_NAME):
    with MongoClient() as client:
        return list(client[db_name][REVIEWED].find())


def get_article(article, db_name=DB_NAME):
    return get_article_full(article.title, db_name=db_name)


def get_article_full(title, db_name=DB_NAME):
    with MongoClient() as client:
        return client[db_name][REVIEWED].find_one({
            "title": title.lower()
        })


def repair(db_name=DB_NAME):
    with MongoClient() as client:
        articles = get_articles()
        for article in articles:
            if client[db_name][REVIEWED].find({"title": article["title"]}).count() > 1:
                client[db_name][REVIEWED].remove({"title": article["title"]})
                client[db_name][REVIEWED].update(
                    {
                        "title": article["title"]
                    }, {"$set": {
                        "title": article["title"].lower().strip(),
                        "abstract": article["abstract"],
                        "interest": article["interest"]
                    }}, upsert=True)


if __name__ == "__main__":
    repair()
