import xml.etree.ElementTree as etree


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


filename = 'journey-planner-timetables/one/tfl_3-E10_-33630-y05.xml'
tree = etree.parse(filename)
lineName = findOffspring(tree, 'LineName').text
print(lineName)

stopPoints = findChild(tree, 'StopPoints').getchildren()
print(stopPoints.getchildren())


# journeyPatternSections = findChild(tree, 'JourneyPatternSections')
# journeyPatternSection = journeyPatternSections.getchildren()[0]
# journeyPatternTimingLinks = journeyPatternSection.getchildren()

# # print(*journeyPatternTimingLinks, sep='\n')

# for link in journeyPatternTimingLinks:
#     # print(link.get('id'))
#     fromStop, toStop, runTime = findChildren(link, ['From', 'To', 'RunTime'])
#     stops = list(map(getStopPointRef, [fromStop, toStop]))
#     print(stops, runTime.text)
