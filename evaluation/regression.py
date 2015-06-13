import pickle
import os
from sklearn import linear_model
import numpy
from numpy import std


def load_test_cases():
    if os.path.isfile("test_cases.p"):
        return pickle.load(open("test_cases.p", "rb"))
    else:
        return []


def findCoef():
    cases = load_test_cases()
    xs = [list(c)[0:3] for c in cases]
    ys = [c[3] for c in cases]

    clf = linear_model.LinearRegression()
    clf.fit(xs, ys)
    print(clf.coef_)


def printError():
    cases = load_test_cases()
    print(len(cases))
    count = 0
    for c in cases:
        # print (c[8], c[7])
        if abs(c[8]) <= abs(c[7]):
            count += 1
    print(count)

    print(std([c[8] for c in cases]))

printError()
