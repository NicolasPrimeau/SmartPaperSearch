import sys
from mendeley import Mendeley
import yaml
import os
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.utils.validation import NotFittedError
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import words
import pickle

config_file = 'config/config.yml'
resources_file = 'config/resources.yml'
classifier_file = "config/classifier.mdl"

learning_rate = 0.01

unique = set(words.words())


def get_classifier():
    clf = PassiveAggressiveClassifier(loss='squared_hinge', C=1.0)
    return clf


def get_features(text):
    count_vect = CountVectorizer(analyzer='char_wb', ngram_range=(1, 5), min_df=1,
                                 vocabulary=unique)
    X_train_counts = count_vect.fit_transform([text])
    tfidf_transformer = TfidfTransformer()
    return tfidf_transformer.fit_transform(X_train_counts)


def clear():
    print(chr(27) + "[2J")


def main():

    if os.path.isfile(config_file):
        with open(config_file) as f:
            config = yaml.load(f)
    else:
        raise ValueError("Need config file")

    if os.path.isfile(resources_file):
        with open(resources_file) as f:
            resources = yaml.load(f)
    else:
        raise ValueError("Need resources file")

    clf = load()

    mendeley = Mendeley(config['clientId'], config['clientSecret'])
    session = mendeley.start_client_credentials_flow().authenticate()

    docs = session.catalog.search(query=resources['query'], view='bib')
    
    for doc in docs.iter():
        """
        Doc Has:
        id, title, type, source, year, identifies, resources, abstract, link, authors, files
        pages, volumne, issue, websites, month, publisher, day, city, edition, instituion, series,
        chapter, revision, accessed, editors
        """

        if doc.type not in resources['unwanted']:
            features = get_features(doc.abstract.replace("-\\n", "").replace("- \\n", "").replace("\\n", " "))
            try:
                interesting = clf.predict(features)
                power = clf.decision_function(features)
            except NotFittedError:
                interesting = None
                power = None
                pass
            if power > -2:
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
                x = input("Interesting? (y/n) ")
                if x == "n" or x == '0':
                    clf.partial_fit(features, [0], [0, 1])
                elif x == "n" or x == '1':
                    clf.partial_fit(features, [1], [0, 1])
                elif x == "q":
                    save(clf)
                    break
                clear()


def save(clf):
    global classifier_file
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
    line = line.replace("-\\n", "").replace("\\n", " ")
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
    main()
