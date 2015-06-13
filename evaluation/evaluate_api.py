import requests
import random_url
import sys
import json
import time
import pickle
import os
import datetime


def connect(url):
    r = requests.get(url)
    # print("Status Code:", r.status_code)

    if r.status_code != requests.codes.ok:
        print("Received a bad status code from the server -- aborting")
        print(r.text)
        # sys.exit()
    return r


def getPageResult(res):
    return json.loads(res.text)['results']


def getArrivalList(key, source):
    return sorted([entry[key] for entry in source])


def getStops(predictions):
    stops = [(entry['sequence'], entry['stop_code_lbsl'])
             for entry in predictions]
    sorted(stops, key=lambda x: x[0])
    stops = [x[1] for x in stops]
    return stops


def getTime(l):
    return datetime.datetime.fromtimestamp(int(l / 1000))


def getPredictions(pre_res, tfl_res):
    predictions = getPageResult(pre_res)
    tfl_timetable = getPageResult(tfl_res)

    stops = getStops(predictions)

    historical = getArrivalList('cumulative_travel_time', predictions)
    current = getArrivalList('curr_cumulative_travel_time', predictions)
    reference = getArrivalList('cumulative_travel_time', tfl_timetable)
    return (historical, current, reference, stops)


def connect_to_countdown(route, run, naptan_atco):
    url = ("http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?"
           "LineName={}&DirectionID={}&StopCode2={}&"
           "ReturnList=StopID,LineName,DirectionID,VehicleID,TripID,"
           "EstimatedTime,ExpireTime")
    url = url.format(route, run, naptan_atco)
    # print(url)
    r = requests.get(url, auth=('LiveBus95085', 'rU9HUx4ZEm'))
    # print("Status Code:", r.status_code)

    if r.status_code != requests.codes.ok:
        print("Received a bad status code from the server -- aborting")
        print(r.text)
        # sys.exit()
    return r


def getCountdowns(r):
    buses = []
    for line in r.iter_lines():
        if not line:
            continue
        line = json.loads(line.decode('utf-8-sig'))
        if line[0] != 1:
            continue
        line = line[1:]
        buses.append(line)
    return buses


def getNextVehicle(countdown_res):
    # next_vehicles = []
    # while next_vehicles == []:
        # print("Getting countdowns...")
        # print(countdown_res)
        # print(len(countdown_res.lines()))
    next_vehicles = getCountdowns(countdown_res)
    sorted(next_vehicles, key=lambda x: x[5])
    if not next_vehicles:
        return []
    nxt = next_vehicles[0]
    vehicle = {}
    vehicle['stop_code_lbsl'] = nxt[0]
    vehicle['route'] = nxt[1]
    vehicle['run'] = nxt[2]
    vehicle['vehicle_id'] = nxt[3]
    vehicle['trip_id'] = nxt[4]
    vehicle['arrival_time'] = nxt[5]
    return vehicle


def load_current_predictions():
    if os.path.isfile("evaluate_api.p"):
        return pickle.load(open("evaluate_api.p", "rb"))
    else:
        return {}


def updateRecord(record, pre_res, tfl_res, countdown_res,
                 params, next_vehicle, record_time):
    print("Getting predictions")
    historical, current, reference, stops = getPredictions(pre_res, tfl_res)
    record_key = (params['day'], params['hour'], params['route'],
                  params['run'], params['naptan_atco'])
    record[record_key] = {'historical': historical,
                          'current': current,
                          'reference': reference,
                          'pre_url': pre_url,
                          'tfl_url': tfl_url,
                          'next_vehicle': next_vehicle,
                          'stops': stops,
                          'record_time': record_time}
    return record


for i in range(100):
    record = load_current_predictions()
    next_vehicle = []
    try:
        while not next_vehicle:
            pre_url, tfl_url, params = random_url.getCurrentURLs()

            print("Connecting to TfL countdown")
            print(params)
            countdown_res = connect_to_countdown(params['route'],
                                                 params['run'],
                                                 params['naptan_atco'])
            next_vehicle = getNextVehicle(countdown_res)
            record_time = time.time()
            print('next_vehicle')
            print(next_vehicle)
            if countdown_res.status_code != requests.codes.ok:
                continue
            if not next_vehicle:
                continue

            if getTime(next_vehicle['arrival_time']) - datetime.datetime.now() > datetime.timedelta(minutes=5):
                continue
                print('next loop')

            print("Connecting to endpoints")
            pre_res, tfl_res = connect(pre_url), connect(tfl_url)
            if pre_res.status_code != requests.codes.ok:
                continue
            if tfl_res.status_code != requests.codes.ok:
                continue

            print("Updating record")
            print(countdown_res.text)
            record = updateRecord(record, pre_res, tfl_res, countdown_res,
                                  params, next_vehicle, record_time)
            print(len(record))
            print("Saving to pickle")
            pickle.dump(record, open("evaluate_api.p", "wb"))
            print("Finish")
    except ValueError:
        print("Error,")
