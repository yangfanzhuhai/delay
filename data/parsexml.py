import xml.etree.ElementTree as etree
from collections import defaultdict


def getElementName(name):
    return '{}{}'.format('{http://www.transxchange.org.uk/}', name)


def getElementNameR(name):
    return '{}{}'.format('.//{http://www.transxchange.org.uk/}', name)


def findChild(parent, childName):
    return parent.find(getElementName(childName))


def findChildren(parent, childrenNames):
    return list(map(lambda x: findChild(parent, x), childrenNames))


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
    # print(link.get('id'))
    result = {}
    fromStop = findChild(TimingLinkElement, 'From')
    toStop, runTime = findChildren(TimingLinkElement, ['To', 'RunTime'])
    fromStopRef = getStopPointRef(fromStop)
    result['from'] = stops[fromStopRef][1][0].text
    # result['fromSequence'] = fromStop.get('SequenceNumber')
    # result['runTime'] = runTime.text
    toStopRef = getStopPointRef(toStop)
    result['to'] = stops[toStopRef][1][0].text
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


def getVehicleJourneys(tree):
    vjs = findChild(tree, 'VehicleJourneys')
    vehicleJourneys = defaultdict(lambda: defaultdict(dict))
    # vehicleJourneys = defaultdict(dict)
    for vj in vjs:
        destination, jpRef, departureTime = findChildren(vj,
                                                         ['DestinationDisplay',
                                                          'JourneyPatternRef',
                                                          'DepartureTime'])
        days = vj[3][0][0][0].tag.split('}', 1)[1]
        run = jpRef.text[-1]
        # dict.get(key, default=None)
        vehicleJourneys[run][days][departureTime.text] = getJourneyPatternSectionRef(jpRef.text)
    return vehicleJourneys


def getJourneyPatternSectionRef(s):
    # 'JP_21-C3-_-y05-38492-33-I-2' becomes
    # 'JPS_21-C3-_-y05-38492-33-2-I'
    return s[:2] + 'S' + s[2:-3] + s[-1] + s[-2] + s[-3]

filename = 'journey-planner-timetables/one/tfl_21-C3_-38492-y05.xml'
tree = etree.parse(filename)
lineName = findOffspring(tree, 'LineName').text
print(lineName)

stops = getStopNames(tree)
journeyPatterns = getJourneyPatterns(tree)
vehicleJourneys = getVehicleJourneys(tree)

sat1 = vehicleJourneys['2']['Saturday']
departureTime, journeyPatternRef = list(sat1.items())[0]
print (departureTime, journeyPatternRef)

jps = journeyPatterns[journeyPatternRef]
route = list(map(lambda x: getRunTime(x, stops), jps))

print (route)
