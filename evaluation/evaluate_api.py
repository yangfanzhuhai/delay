import requests
import random_url
import sys
import json
import datetime


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


def getPredictions(pre_url, tfl_url):
    pre_res, tfl_res = connect(pre_url), connect(tfl_url)
    predictions = getPageResult(pre_res)
    tfl_timetable = getPageResult(tfl_res)

    historical = getArrivalList('cumulative_travel_time', predictions)
    current = getArrivalList('curr_cumulative_travel_time', predictions)
    reference = getArrivalList('cumulative_travel_time', tfl_timetable)
    return (historical, current, reference)


def connect_to_countdown(route, run, naptan_atco):
    url = ("http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?"
           "LineName={}&DirectionID={}&StopCode2={}&"
           "ReturnList=StopID,LineName,DirectionID,VehicleID,TripID,"
           "EstimatedTime,ExpireTime")
    url = url.format(route, run, naptan_atco)
    print(url)
    r = requests.get(url, auth=('LiveBus95085', 'rU9HUx4ZEm'))
    print("Status Code:", r.status_code)

    if r.status_code != requests.codes.ok:
        print("Received a bad status code from the server -- aborting")
        print(r.text)
        sys.exit()
    return r


def getTime(l):
    return datetime.datetime.fromtimestamp(int(l / 1000))


def getCountdowns(r):
    buses = []
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
        buses.append(line)
    return buses


def getNextVehicle(params):
    countdown_res = connect_to_countdown(params['route'], params['run'],
                                         params['naptan_atco'])

    next_vehicles = []
    while next_vehicles == []:
        next_vehicles = getCountdowns(countdown_res)
    sorted(next_vehicles, key=lambda x: x[5])
    return next_vehicles[0]


def updateRecord(record, pre_url, tfl_url, params):
    historical, current, reference = getPredictions(pre_url, tfl_url)
    record_key = (params['day'], params['hour'], params['route'],
                  params['run'], params['naptan_atco'])
    record[record_key] = {'historical': historical,
                          'current': current,
                          'reference': reference,
                          'pre_url': pre_url,
                          'tfl_url': tfl_url}
    return record


record = {}
pre_url, tfl_url, params = random_url.getCurrentURLs()
record = updateRecord(record, pre_url, tfl_url, params)
print(record)

next_vehicle = getNextVehicle(params)
print(next_vehicle)



