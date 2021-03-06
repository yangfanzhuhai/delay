import requests
import json
import pymysql
import sys
import datetime
import time
import pickle
import os.path
import threading


def connect_to_countdown():
    url = ("http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?"
           "ReturnList=StopID,LineName,DirectionID,VehicleID,TripID,"
           "EstimatedTime,ExpireTime")

    r = requests.get(url, auth=('LiveBus95085', 'rU9HUx4ZEm'))
    print("Status Code:", r.status_code)

    if r.status_code != requests.codes.ok:
        print("Received a bad status code from the server -- aborting")
        print(r.text)
        sys.exit()
    return r


def load_current_arrivals():
    if os.path.isfile("arrival.p"):
        return pickle.load(open("arrival.p", "rb"))
    else:
        return {}


def getTime(l):
    return datetime.datetime.fromtimestamp(int(l / 1000))


def update_current(r, arrival):
    for line in r.iter_lines():
        if not line:
            continue
        line = json.loads(line.decode('utf-8-sig'))
        if line[0] != 1:
            continue
        line = line[1:]
        line[5] = getTime(line[5])
        if int(line[6]/1000) == 0:
            line[6] = None
            print("has none")
        else:
            line[6] = getTime(line[6])
        line.append(line[5])
        arrival[tuple(line[0:5])] = line
    return arrival


def connect_to_db():
    conn = pymysql.connect(
        host='localhost',
        # host='delay.doc.ic.ac.uk',
        port=3306,
        user='delay',
        passwd='CcwLCw3Kcs9Py33T',
        db='delay')
    return conn


def insert_arrivals_to_db(conn, arrival):
    cur = conn.cursor()
    sql_insert = ("INSERT INTO current_arrivals "
                  "(stop_code_lbsl, route, run, vehicle_id, trip_id, "
                  "arrival_time, expire_time, arrival_date) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, DATE(%s)) ")
    print(len(arrival))
    expired = [v for v in arrival.values()
               if (v[6] is None or
                   (v[6] + datetime.timedelta(minutes=15)
                    <= datetime.datetime.now()))]

    print("filtered expired")
    print(len(expired))
    arrival = dict((k, v) for k, v in arrival.items()
                   if (v[6] is not None and
                       (v[6] + datetime.timedelta(minutes=15)
                        > datetime.datetime.now())
                       )
                   )
    print("filtered arrival")
    for line in expired:
        # print(line[0:5], line[5].strftime("%H:%M:%S"), line[6])
        # print(line)
        cur.execute(sql_insert, line[0:8])
    return arrival


def f():
    tic = time.clock()
    r = connect_to_countdown()
    arrival = load_current_arrivals()
    print("loaded current")
    arrival = update_current(r, arrival)
    print("updated current")
    conn = connect_to_db()
    print("connected to db")
    arrival = insert_arrivals_to_db(conn, arrival)
    conn.commit()
    conn.close()
    pickle.dump(arrival, open("arrival.p", "wb"))
    toc = time.clock()
    print(toc - tic)
    threading.Timer(15, f).start()

# start calling f now and every 60 sec thereafter
f()
