#!/usr/bin/env python3

from collections import Counter
import urllib.request
from lxml import etree

import numpy as np

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn import model_selection

alphabet="abcdefghijklmnopqrstuvwxyzäö-"
alphabet_set = set(alphabet)

# Returns a list of Finnish words
def load_finnish():
    finnish_url="https://www.cs.helsinki.fi/u/jttoivon/dap/data/kotus-sanalista_v1/kotus-sanalista_v1.xml"
    filename='src/kotus-sanalista_v1.xml'
    load_from_net=False
    if load_from_net:
        with urllib.request.urlopen(finnish_url) as data:
            lines=[]
            for line in data:
                lines.append(line.decode('utf-8'))
        doc="".join(lines)
    else:
        with open(filename, "rb") as data:
            doc=data.read()
    tree = etree.XML(doc)
    s_elements = tree.xpath('/kotus-sanalista/st/s')
    return list(map(lambda s: s.text, s_elements))

# Returns a list of English words
def load_english():
    with open("src/words", encoding="utf-8") as data:
        lines=map(lambda s: s.rstrip(), data.readlines())
    return lines

def get_features(words):
    start = np.empty([0, 29])
    character = np.zeros(29)
    alphabet_list = list(alphabet)
    for word in words:
        for order, letter in enumerate(alphabet_list):
            if letter in word:
                character[order] += 1
        result = np.vstack((start, character))
        start = result
    return result

def contains_valid_chars(s):
    sub = set(s)
    if len(sub - alphabet_set) == 0:
        return True
    else:
        return False

def get_features_and_labels():
    # Filter Finnish word list
    finnish = load_finnish()
    finnish = [i.lower() for i in finnish]
    filter_finnish = list(filter(lambda x: contains_valid_chars(x) == True, finnish))

    # Filter English word list
    english = list(load_english())
    proper_nouns = [word for word in english if word[0].isupper()]
    filter_proper_nouns = [item for item in english if item not in proper_nouns]
    lowercase_english = [i.lower() for i in filter_proper_nouns]
    filter_english = list(filter(lambda x: contains_valid_chars(x) == True, lowercase_english))

    filter_finnish.extend(filter_english)
    y = []
    samples = []

    #Get feature and target vector
    X = get_features(filter_finnish)
    for word in filter_finnish:
        if word in filter_english and word not in samples:
            y.append(1)
            samples.append(word) # Avoid including duplicated words in filter_finnish
        else:
            y.append(0)
    y = np.array(y)
    return X, y

def word_classification():
    X, y = get_features_and_labels()
    model = MultinomialNB()
    model.fit(X, y)
    #cv = model_selection.KFold(n_splits=5, shuffle=True, random_state=0)
    #return cross_val_score(model, X, y, cv=cv)
    return cross_val_score(model, X, y)


def main():
    # x,y = get_features_and_labels()
    # print(len(x.shape))
    # print(x.shape, y.shape[0])
    # print(sum(y))
    print("Accuracy scores are:", word_classification())

if __name__ == "__main__":
    main()
