import pickle
import os
import datetime
import pymysql
from numpy import std


def load_current_predictions():
    if os.path.isfile("evaluate_api.p"):
        return pickle.load(open("evaluate_api.p", "rb"))
    else:
        return {}


def getTime(l):
    return datetime.datetime.fromtimestamp(int(l / 1000))


def connect_to_db():
    conn = pymysql.connect(
        # host='localhost',
        host='delay.doc.ic.ac.uk',
        port=3306,
        user='delay',
        passwd='CcwLCw3Kcs9Py33T',
        db='delay')
    # print('connected to db')
    return conn


def getActualArrivals(res, stops):
    actual = {}
    arrival_list = []
    for entry in res:
        actual[entry[0]] = entry[5]
    for stop in stops:
        if stop in actual.keys():
            arrival_list.append(actual[stop])
        else:
            arrival_list.append(0)
    return arrival_list


def getDiff(pre, act):
    return (pre - act).seconds + (pre - act).days * 24 * 3600
    # return pre - act


def getPre(arrival_time, pre):
    return (arrival_time + datetime.timedelta(seconds=float(pre))).timestamp()


def getSTDs(diffs):
    return(std([entry[6] for entry in diffs]),
           std([entry[7] for entry in diffs]),
           std([entry[8] for entry in diffs]),
           std([entry[9] for entry in diffs]))


def printTitle(value, route, vehicle, naptan_code):
    print('recorded_time',
          datetime.datetime.fromtimestamp(value['record_time']))
    print('route', route, 'stop', vehicle['stop_code_lbsl'], naptan_code)
    print('historical, current, reference, actual,',
          'delta_historical, delta_current, delta_reference, stop')
    print(vehicle)


def addToDiffs(historical, current, reference, actual_arrivals, diffs,
               arrival_time):
    his = getPre(arrival_time, historical)
    curr = getPre(arrival_time, current)
    ref = getPre(arrival_time, reference)
    act = actual_arrivals.timestamp()

    combine = 0.01546162 * float(historical) - 0.01909407 * float(current) + 1.07500769 * reference
    comb = getPre(arrival_time, combine)

    k = (float(historical),
         float(current),
         reference,
         combine,
         getDiff(actual_arrivals, arrival_time),
         his - act,
         curr - act,
         ref - act,
         comb - act)
    # print(k)
    diffs.append(k)
    return diffs
    # print(his.strftime('%H:%M:%S'),
    #       curr.strftime('%H:%M:%S'),
    #       ref.strftime('%H:%M:%S'),
    #       act.strftime('%H:%M:%S'),
    #       diffs[-1],
    #       stop)


def processTestCase(key, value, count, cases, cur, sql):
    day, hour, route, run, naptan_code = key
    vehicle = value['next_vehicle']
    arrival_time = getTime(vehicle['arrival_time'])
    stops = value['stops']
    # printTitle(value, route, vehicle, naptan_code)

    cur.execute(sql, [vehicle['run'], vehicle['route'],
                      vehicle['vehicle_id'], vehicle['trip_id']])
    actual_arrivals = getActualArrivals(cur.fetchall(), stops)

    diffs = []
    for index, stop in enumerate(stops):
        try:
            if actual_arrivals[index]:
                addToDiffs(value['historical'][index],
                           value['current'][index],
                           value['reference'][index],
                           actual_arrivals[index], diffs, arrival_time)
        except IndexError:
            continue
    if not diffs:
        return (count, cases)
    cases.extend(diffs)
    return (count, cases)


def getTestCases():
    records = load_current_predictions()
    conn = connect_to_db()
    cur = conn.cursor()
    sql = ("SELECT * FROM current_arrivals "
           "WHERE run = %s AND route = %s AND vehicle_id = %s "
           "AND trip_id = %s")

    count = 0
    cases = []
    for key, value in records.items():
        count, cases = processTestCase(key, value, count, cases, cur, sql)
    print(count)
    return cases

cases = getTestCases()
print(cases)
print(len(cases))
pickle.dump(cases, open("test_cases.p", "wb"))

