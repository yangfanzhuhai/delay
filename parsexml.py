import xml.etree.ElementTree as etree
from collections import defaultdict
from itertools import accumulate
import datetime as dt
import csv
import os


def getElementName(name):
    return '{}{}'.format('{http://www.transxchange.org.uk/}', name)


def getElementNameR(name):
    return '{}{}'.format('.//{http://www.transxchange.org.uk/}', name)


def findChild(parent, childName):
    return parent.find(getElementName(childName))


def findAllChildWithSameName(parent, childName):
    return parent.findall(getElementName(childName))


def findChildren(parent, childrenNames):
    return [findChild(parent, x) for x in childrenNames]


def findOffspring(parent, childName):
    return parent.find(getElementNameR(childName))


def getStopPointRef(subTimingLink):
    return findChild(subTimingLink, 'StopPointRef').text


def getTimeInSeconds(ptTime):
    time = ptTime[2:-1].split('M')
    if len(time) == 1:
        return int(time[0])
    else:
        return int(time[0]) * 60 + int(time[1])


def getRunTime(TimingLinkElement, stops):
    result = {}
    fromStop = findChild(TimingLinkElement, 'From')
    toStop, runTime = findChildren(TimingLinkElement, ['To', 'RunTime'])
    fromStopRef = getStopPointRef(fromStop)
    result['from'] = stops[fromStopRef][1][0].text
    result['fromStopRef'] = fromStopRef
    # result['fromSequence'] = fromStop.get('SequenceNumber')
    # result['runTime'] = runTime.text
    toStopRef = getStopPointRef(toStop)
    result['to'] = stops[toStopRef][1][0].text
    result['toStopRef'] = toStopRef
    result['toSequence'] = toStop.get('SequenceNumber')
    result['travelTime'] = getTimeInSeconds(runTime.text)
    return result


def getStopNames(tree):
    # build stops dictionary (StopPointRef, StopPoint Element)
    stopPointElements = findChild(tree, 'StopPoints')
    stops = {}
    for child in stopPointElements:
        stops[child[0].text] = child
    return stops


def getJourneyPatterns(tree):
    # build journey pattern dictionary
    journeyPatternSection = findChild(tree, 'JourneyPatternSections')
    jps = {}
    for child in journeyPatternSection:
        jps[child.get('id')] = child
    return jps


def getDaysOfWeek(parent):
    operatingProfile = findChild(parent, 'OperatingProfile')
    regularDayType = findChild(operatingProfile, 'RegularDayType')
    daysOfWeek = findChild(regularDayType, 'DaysOfWeek')
    return daysOfWeek[0].tag.split('}', 1)[1]


def getDefaultDays(tree):
    service = findChild(tree, 'Services')[0]
    return getDaysOfWeek(service)


def getRunFromJourneyPatternRef(jpRef):
    split = jpRef.text.split('-')
    if split[-2] == 'O':
        return 1
    elif split[-2] == 'I':
        return 2
    return 0


def getVehicleJourneys(tree, defaultDays, jpRefToJpsRef):
    vjElements = findChild(tree, 'VehicleJourneys')
    vjs = defaultdict(lambda: defaultdict(dict))
    for vj in vjElements:
        destination, jpRef, departureTime = findChildren(vj,
                                                         ['DestinationDisplay',
                                                          'JourneyPatternRef',
                                                          'DepartureTime'])
        if findOffspring(vj, 'OperatingProfile') is not None:
            days = getDaysOfWeek(vj)
        else:
            days = defaultDays

        run = getRunFromJourneyPatternRef(jpRef)
        vjs[run][days][departureTime.text] = jpRefToJpsRef[jpRef.text]
    return vjs


def getJourneyPatternIDMap(tree):
    m = {}
    service = findChild(tree, 'Services')[0]
    standardService = findChild(service, 'StandardService')
    journeyPatterns = findAllChildWithSameName(standardService,
                                               'JourneyPattern')
    for jp in journeyPatterns:
        m[jp.get('id')] = findChild(jp, 'JourneyPatternSectionRefs').text
    return m


def appendOrigin(route):
    head = route[0].copy()
    head['to'] = head['from']
    head['toSequence'] = 1
    head['arrivalTime'] = head['departure_time']
    head['cummulativeTravelTime'] = 0
    head['toStopRef'] = head['fromStopRef']
    route.insert(0, head)
    return route


def getEntries(lineName, day, run, journeyPatternRef,
               departureTime, journeyPatterns, stops):
    route = []
    departureTime = dt.datetime.strptime(departureTime, '%H:%M:%S').time()
    departureDt = (dt.datetime.combine(dt.date(1, 1, 1), departureTime))

    jps = journeyPatterns[journeyPatternRef]
    route = [getRunTime(x, stops) for x in jps]
    travelTimes = [x['travelTime'] for x in route]
    accTravelTimes = list(accumulate(travelTimes))
    for x, entry in enumerate(route):
        entry['cummulativeTravelTime'] = accTravelTimes[x]
        delta = dt.timedelta(seconds=accTravelTimes[x])
        entry['arrivalTime'] = (departureDt +
                                delta).time().strftime("%H:%M:%S")
        entry['line_name'] = lineName
        entry['day'] = day
        entry['run'] = run
        entry['departure_time'] = departureTime
    route = appendOrigin(route)
    return route


def saveToFile(route, lineName):
    filename = 'generated/tfl_timetables/tfl_timetable_{}.csv'.format(lineName)
    with open(filename, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['line_name', 'day', 'run', 'sequence', 'naptan_atco',
                         'stop_name', 'departure_time_from_origin',
                         'arrival_time', 'cummulative_travel_time'])
        for entry in route:
            writer.writerow([entry['line_name'], entry['day'],
                             entry['run'], entry['toSequence'],
                             entry['toStopRef'],
                             entry['to'], entry['departure_time'],
                             entry['arrivalTime'],
                             entry['cummulativeTravelTime']])


def generateArrivalEntries(filename):
    tree = etree.parse(filename)
    lineName = findOffspring(tree, 'LineName').text
    print('processing', lineName)
    stops = getStopNames(tree)
    journeyPatterns = getJourneyPatterns(tree)
    jpRefToJpsRef = getJourneyPatternIDMap(tree)
    defaultDays = getDefaultDays(tree)
    vehicleJourneys = getVehicleJourneys(tree, defaultDays, jpRefToJpsRef)
    route = []

    for run in vehicleJourneys.keys():
        for day in vehicleJourneys[run].keys():
            for departureTime in vehicleJourneys[run][day].keys():
                journeyPatternRef = vehicleJourneys[run][day][departureTime]
                route.extend(getEntries(lineName, day, run, journeyPatternRef,
                                        departureTime, journeyPatterns, stops))

    saveToFile(route, lineName)


directory = 'data/journey-planner-timetables/one/'
# for filename in os.listdir(directory):
#     if filename.endswith(".xml"):
#         print (filename)
#         filename = directory + filename
#         generateArrivalEntries(filename)


generateArrivalEntries(directory + 'tfl_21-U7_-25184-y05.xml')
