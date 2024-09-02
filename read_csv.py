import csv


def read_csv(path):
    articles = []
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            articles.append(row)
    return articles
