import pickle
import os
import datetime
import pymysql
from numpy import std


def load_current_predictions(f):
    if os.path.isfile(f):
        return pickle.load(open(f, "rb"))
    else:
        return {}


def printTime(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')


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


def processTestCase(key, value, count, cases, cur, sql):
    day, hour, route, run, naptan_code = key
    vehicle = value['next_vehicle']
    arrival_time = getTime(vehicle['arrival_time'])
    stops = value['stops']
    # printTitle(value, route, vehicle, naptan_code)
    # print(key)
    cur.execute(sql, [vehicle['run'], vehicle['route'],
                      vehicle['vehicle_id'], vehicle['trip_id']])
    actual_arrivals = getActualArrivals(cur.fetchall(), stops)

    # print(key)
    # print(vehicle)

    diffs = []
    for index, stop in enumerate(stops):
        try:
            if actual_arrivals[index]:

                diffs.append((float(value['historical'][index]),
                             float(value['current'][index]),
                             value['reference'][index],
                             getDiff(actual_arrivals[index], arrival_time)))
                # if vehicle['vehicle_id'] == 16094 and vehicle['trip_id'] == 73487:

                # if float(value['current'][index]) - getDiff(actual_arrivals[index], arrival_time) >= 900:
                print()
                print(value)
                print('stop', stop)
                v = value
                i = index
                record_time = float(v['record_time'])
                his = record_time + float(v['historical'][i])
                cur = record_time + float(v['current'][i])
                ref = record_time + float(v['reference'][i])
                his = printTime(his)
                cur = printTime(cur)
                ref = printTime(ref)
                print (his, cur, ref, actual_arrivals[index])
                print (float(value['historical'][index]), float(value['current'][index]), value['reference'][index])
                print(float(value['current'][index]) - getDiff(actual_arrivals[index], arrival_time))
        except IndexError:
            continue
    if not diffs:
        return (count, cases)
    cases.extend(diffs)
    return (count, cases)


def getTestCases(f):
    print('getTestCases')
    records = load_current_predictions(f)
    print('loaded Records')
    conn = connect_to_db()
    print('connected to db')
    cur = conn.cursor()
    sql = ("SELECT * FROM current_arrivals "
           "WHERE run = %s AND route = %s AND vehicle_id = %s "
           "AND trip_id = %s")

    count = 0
    cases = []
    for key, value in records.items():
        # print(key)
        count, cases = processTestCase(key, value, count, cases, cur, sql)
    print(count)
    return cases

cases = getTestCases("evaluate_api.p")
print(cases)
print(len(cases))
pickle.dump(cases, open("test_cases.p", "wb"))

