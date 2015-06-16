import pickle
import os
from sklearn import linear_model
import numpy
from numpy import std
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


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
    return clf.coef_


def printPercentile(ref_errs, comb_errs):
    percent = [5, 10, 20, 30, 40, 44, 45, 50, 60, 70, 80, 90, 95, 99]
    for p in percent:
        print('percentiles', p, 'ref', 'comb')
        print(np.percentile(ref_errs, p), np.percentile(comb_errs, p))
        print()


def filterOutliers(errs):
    return np.array([e for e in errs if e < 2000 and e >= -2000])


def printError():
    cases = load_test_cases()
    # print(len(cases))
    count = 0
    ref_errs = np.array([c[2] - c[3] for c in cases])
    his_errs = np.array([c[0] - c[3] for c in cases])
    curr_errs = np.array([c[1] - c[3] for c in cases])
    # comb_errs = np.array([c[0] * coe[0] + c[1] * coe[1] + c[2] * coe[2] - c[3] for c in cases])

    ref_errs = filterOutliers(ref_errs)
    his_errs = filterOutliers(his_errs)
    curr_errs = filterOutliers(curr_errs)

    # printPercentile(ref_errs, curr_errs)

    sns.kdeplot(ref_errs, label='TfL Reference Timetable')
    sns.kdeplot(his_errs, label='Historical Timetable')
    sns.kdeplot(curr_errs, label='Current Timetable')
    # sns.kdeplot(comb_errs, label='Combine Timetable')
    plt.xlabel('Active Traffic Delay Predictions - Actual Bus Journey Times (s)')
    plt.ylabel('Probability Distribution')
    # plt.hist(comb_errs, 20, color="#F08080", alpha=.5)
    plt.savefig('prediction_accuracy.png')

    # minutes = list(range(15))
    # for m in minutes:
    #     print('delay limit', m)
    # for c in cases:
    #     ref_err =
    #     comb_err =
    #     # if abs(comb_err) <= abs(ref_err) + 60:
    #     #     count += 1
    #     if comb_err > 600:
    #         count += 1
    # print(count)
# coe = findCoef()
printError()

