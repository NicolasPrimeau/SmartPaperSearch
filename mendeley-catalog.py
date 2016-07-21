import datetime
import sys
from threading import Thread

import yaml
import os

from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.utils.validation import NotFittedError
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import words
import pickle

import DatabaseDAO
import auth_fetcher

config_file = 'config/config.yml'
resources_file = 'config/resources.yml'
classifier_file = "config/classifier.mdl"
power_threshold = -3
learning_rate = 0.1

unique = set(words.words())


def get_classifier():
    clf = PassiveAggressiveClassifier(loss='squared_hinge', C=1.0)
    return clf


def get_features(text):
    count_vect = CountVectorizer(analyzer='char_wb', ngram_range=(1, 5), min_df=1,
                                 vocabulary=unique)
    if isinstance(text, list):
        x_train_counts = count_vect.fit_transform(text)
    else:
        x_train_counts = count_vect.fit_transform([text])
    tfidf_transformer = TfidfTransformer()
    return tfidf_transformer.fit_transform(x_train_counts)


def clear():
    print(chr(27) + "[2J")


def startup_learn(classifier):
    print("Startup Learning...")
    abstracts = list()
    interest = list()
    for article in DatabaseDAO.get_articles():
        try:
            abstracts.append(article["abstract"])
        except KeyError:
            print(article)
            sys.exit()
        interest.append(int(article["interest"]))
    if len(abstracts) == 0:
        return
    classifier.partial_fit(get_features(abstracts), interest, [0, 1])
    print("Done! Learned on " + str(len(abstracts)) + " documents")


def main():

    if os.path.isfile(resources_file):
        with open(resources_file) as f:
            resources = yaml.load(f)
    else:
        raise ValueError("Need resources file")

    print("Need Authorization, go logon at http://localhost:5000/!")
    session = auth_fetcher.get_session_from_cookies()
    clf = load()
    startup_learn(clf)
    while iterate(session, clf, resources):
        save(clf)


def iterate(session, clf, resources):
    global power_threshold
    print("Power Threshold: " + str(power_threshold))
    clear()
    query = input("What's the search query? ")
    clear()
    docs = session.catalog.search(query=query, view='bib')
    for doc in docs.iter():
        """
        Doc Has:
        id, title, type, source, year, identifies, resources, abstract, link, authors, files
        pages, volumne, issue, websites, month,     interesting = DatabaseDAO.get_interesting()publisher, day, city,
        edition, instituion, series, chapter, revision, accessed, editors
        """
        print(str(datetime.datetime.now()) + " -- Searching (" + doc.title + ")")
        if doc.type not in resources['unwanted']:
            doc.abstract = doc.abstract.replace("-\\n", "").replace("- \\n", "").replace("\\n", " ")
            doc.title = doc.title.lower()
            features = get_features(doc.abstract)
            try:
                interesting = clf.predict(features)[0]
                power = clf.decision_function(features)[0]
            except NotFittedError:
                interesting = None
                power = None
                pass

            if power > power_threshold and not DatabaseDAO.contains(article=doc):
                clear()
                print("Interest: " + str(interesting) + ", power: " + str(power))
                print()
                print(doc.title)
                print()
                print(doc.year)
                print()
                print(doc.keywords)
                print()
                print(doc.type)
                print()
                print(pretty_format(doc.abstract))
                print()
                decided = False
                skip = False
                while not decided and not skip:
                    x = input("Interesting? (y/n) ")
                    if x == "n" or x == '0':
                        interest = 0
                        decided = True
                    elif x == "y" or x == '1':
                        interest = 1
                        decided = True
                    elif x == "new":
                        return True
                    elif x == "s":
                        skip = True
                        break
                    elif x == "set":
                        command = input("Set Command (Variable=Value) ")
                        variable, value = command.split("=")
                        if variable == "power_threshold":
                            power_threshold = float(value)
                            print("Set Power Threshold to " + str(power_threshold))
                        decided = False
                    elif x == "q":
                        return False
                clear()
                if not skip:
                    clf.partial_fit(features, [interest], [0, 1])
                    DatabaseDAO.save_article(doc, interest)
    return True


def save(clf):
    global classifier_file
    print("Saving Classifier")
    with open(classifier_file, 'wb') as fid:
        pickle.dump(clf, fid)


def load():
    global classifier_file
    if os.path.isfile(classifier_file):
        with open(classifier_file, 'rb') as fid:
            clf = pickle.load(fid)
    else:
        clf = get_classifier()
    return clf


def pretty_format(line, limit=120):
    lines = list()
    start = 0
    end = limit
    while end < len(line):
        while end < len(line) and line[end] != " ":
            end += 1
        lines.append(line[start:end].lstrip())
        start = end
        end += limit
    lines.append(line[start:].lstrip())
    return "\n".join(lines)


if __name__ == "__main__":
    thread = Thread(target=main)
    thread.start()
    auth_fetcher.start()
    thread.join()
