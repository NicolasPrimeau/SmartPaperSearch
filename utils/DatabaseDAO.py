from pymongo import MongoClient

DB_NAME = "MendeleyAutoScrape"
REVIEWED = "articles"
CATEGORIES = "categories"


def reset_category(article, db_name=DB_NAME):
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": cleans_title(article["title"])
            }, {"$unset": {
                "category": 1
            }})


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
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": cleans_title(article["title"])
            }, {"$set": {
                "title": cleans_title(article["title"]),
                "category": categories
            }})


def save_article(article, interest, db_name=DB_NAME):
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": cleans_title(article.title)
            }, {"$set": {
                "title": cleans_title(article.title),
                "abstract": prep_abstract(article.abstract),
                "interest": interest
            }}, upsert=True)


def save_article_full(title, abstract, interest, db_name=DB_NAME):
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": cleans_title(title)
            }, {"$set": {
                "title": cleans_title(title),
                "abstract": prep_abstract(abstract),
                "interest": interest
            }}, upsert=True)


def update_article(title, interest, db_name=DB_NAME):
    with MongoClient() as client:
        client[db_name][REVIEWED].update(
            {
                "title": cleans_title(title)
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
            "title": cleans_title(title.lower())
        })


def prep_abstract(abstract):
    return abstract.replace("-\\n", "").replace("- \\n", "").replace("\\n", " ")


def cleans_title(title):
    return title.lower().strip()


def repair(db_name=DB_NAME):
    with MongoClient() as client:
        for article in client[db_name][REVIEWED].find():
            article["abstract"] = article["abstract"].replace("-\\n", "").replace("- \\n", "").replace("\\n", " ")
            if client[db_name][REVIEWED].find({"title": article["title"]}).count() > 1:
                client[db_name][REVIEWED].remove({"title": article["title"]})
                client[db_name][REVIEWED].update(
                    {
                        "title": cleans_title(article["title"])
                    }, {"$set": {
                        "title": cleans_title(article["title"]),
                        "abstract": article["abstract"],
                        "interest": article["interest"]
                    }}, upsert=True)
            elif "category" in article:
                if not isinstance(article["category"], list):
                    article["category"] = article["category"].split(",")
                client[db_name][REVIEWED].update(
                    {
                        "title": cleans_title(article["title"])
                    }, {"$set": {
                        "title": cleans_title(article["title"]),
                        "abstract": prep_abstract(article["abstract"]),
                        "interest": article["interest"],
                        "category": article["category"]
                    }}, upsert=False)
            else:
                client[db_name][REVIEWED].update(
                    {
                        "title": cleans_title(article["title"])
                    }, {"$set": {
                        "title": cleans_title(article["title"]),
                        "abstract": prep_abstract(article["abstract"]),
                        "interest": article["interest"]
                    }}, upsert=False)

if __name__ == "__main__":
    repair()
