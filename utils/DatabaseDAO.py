from pymongo import MongoClient

DB_NAME = "MendeleyAutoScrape"
REVIEWED = "articles"


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
