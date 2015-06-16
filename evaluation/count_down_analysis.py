import common
import matplotlib as mpl
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import numpy as np
import pickle


def saveDeltaFromDB(cur, table):
    sql = 'SELECT delta FROM ' + table
    cur.execute(sql)
    delta = np.array([item[0] for item in cur.fetchall()])
    pickle.dump(delta, open('tmp/' + table + '.p', "wb"))


def plotDeltas(i, t, range):
    # plt.subplot(4, 2, i)
    delta = common.load('tmp/' + t + '.p', [])
    label = 'Predictions for next {} to {} minutes'.format(range[0], range[1])
    ax = sns.distplot(delta, hist=False, label=label)
    # f.set_title('Predictions for next {} to {} minutes'.format(range[0], range[1]))
    ax.set_xlim([-1000, 1000])
    # plt.xlabel('Prediction - Actual Arrival Time (Seconds)', fontsize=12)
    # plt.ylabel('Probability', fontsize=12)
    # figureTitle = 'figures/' + t + '_graph.png'


def getTableList(ranges):
    tableList = []
    for l, u in ranges:
        tableList.append('predictions_{}_{}_minutes'.format(l, u))
    return tableList


# conn = common.connect_to_db()
# cur = conn.cursor()
ranges = [(0, 3), (0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30)]
tableList = getTableList(ranges)

# for t in tableList:
#     saveDeltaFromDB(cur, t)
# plt.figure(figsize=(10, 15), dpi=80)
# f, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(4, 2, sharex='col', sharey='row')

# axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
plt.figure(figsize=(8, 10))
for i, t in enumerate(tableList):
    plotDeltas(i + 1, t, ranges[i])
plt.xlabel('TfL Live Bus Arrivals API Predictions - Actual Arrivals (s)', fontsize=12)
plt.ylabel('Prbability Distribution', fontsize=12)
plt.savefig('figures/countdown.png')
