import requests
import random_url
import sys
import json
import time
import pickle


def connect(url):
    r = requests.get(url)
    print("Status Code:", r.status_code)

    if r.status_code != requests.codes.ok:
        print("Received a bad status code from the server -- aborting")
        print(r.text)
        sys.exit()
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


def getPredictions(pre_url, tfl_url):
    pre_res, tfl_res = connect(pre_url), connect(tfl_url)
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
    print("Status Code:", r.status_code)

    if r.status_code != requests.codes.ok:
        print("Received a bad status code from the server -- aborting")
        print(r.text)
        sys.exit()
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


def getNextVehicle(params):
    countdown_res = connect_to_countdown(params['route'], params['run'],
                                         params['naptan_atco'])

    next_vehicles = []
    while next_vehicles == []:
        next_vehicles = getCountdowns(countdown_res)
    sorted(next_vehicles, key=lambda x: x[5])
    nxt = next_vehicles[0]
    vehicle = {}
    vehicle['stop_code_lbsl'] = nxt[0]
    vehicle['route'] = nxt[1]
    vehicle['run'] = nxt[2]
    vehicle['vehicle_id'] = nxt[3]
    vehicle['trip_id'] = nxt[4]
    vehicle['arrival_time'] = nxt[5]
    return vehicle


def updateRecord(record, pre_url, tfl_url, params):
    historical, current, reference, stops = getPredictions(pre_url, tfl_url)
    next_vehicle = getNextVehicle(params)
    record_key = (params['day'], params['hour'], params['route'],
                  params['run'], params['naptan_atco'])
    record[record_key] = {'historical': historical,
                          'current': current,
                          'reference': reference,
                          'pre_url': pre_url,
                          'tfl_url': tfl_url,
                          'next_vehicle': next_vehicle,
                          'stops': stops,
                          'record_time': time.time()}
    return record


record = {}
for i in range(100):
    pre_url, tfl_url, params = random_url.getCurrentURLs()
    record = updateRecord(record, pre_url, tfl_url, params)

pickle.dump(record, open("evaluate_api.p", "wb"))
