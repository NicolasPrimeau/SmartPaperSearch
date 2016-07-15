
from mendeley import Mendeley
import yaml
import os

config_file = 'config/config.yml'
resources_file = 'config/resources.yml'


def main():
    config = {}

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
            print(doc.title)
            print(doc.keywords)
            print(doc.type)
            print(pretty_format(doc.abstract))
            x = input()
            if x == "n":
                resources['unwanted'].append(doc.type)


def pretty_format(line, limit=120):
    lines = list()
    start = 0
    end = limit
    while end < len(line):
        while end < len(line) and (line[end] not in ("\n", " ", ",", ".")):
            end += 1
        lines.append(line[start:end].lstrip())
        start = end
        end += limit
    lines.append(line[start:].lstrip())
    return "\n".join(lines)


if __name__ == "__main__":
    main()