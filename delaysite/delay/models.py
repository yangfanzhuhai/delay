from django.db import models
from datetime import datetime


class Neighbours(models.Model):
    route = models.CharField(max_length=64)
    start_stop = models.CharField(max_length=64)
    end_stop = models.CharField(max_length=64)

    def __str__(self):
        return str(self.__dict__)


class Timetable(models.Model):
    start_stop = models.CharField(max_length=64, db_index=True)
    end_stop = models.CharField(max_length=64, db_index=True)
    day = models.CharField(max_length=9, db_index=True)
    hour = models.IntegerField(db_index=True)
    average_travel_time = models.DecimalField(max_digits=11, decimal_places=1)

    def __str__(self):
        return str(self.__dict__)


class Bus_sequences(models.Model):
    route = models.CharField(max_length=64)
    run = models.IntegerField()
    sequence = models.IntegerField()
    stop_code_lbsl = models.CharField(max_length=64)
    bus_stop_code = models.CharField(max_length=64)
    naptan_atco = models.CharField(max_length=64)
    stop_name = models.CharField(max_length=64)
    location_easting = models.IntegerField()
    location_northing = models.IntegerField()
    heading = models.IntegerField()
    virtual_bus_stop = models.IntegerField()
    average_travel_time = models.DecimalField(max_digits=11,
                                              decimal_places=1,
                                              default=0.0)

    def __str__(self):
        return str(self.__dict__)


class Tfl_timetable(models.Model):
    linename = models.CharField(max_length=16, db_index=True)
    day = models.CharField(max_length=32, db_index=True)
    run = models.IntegerField()
    sequence = models.IntegerField()
    stop_name = models.CharField(max_length=64)
    departure_time_from_origin = models.CharField(max_length=64)
    arrival_time = models.CharField(max_length=64)
    cummulative_travel_time = models.IntegerField()


class Arrival(object):

    def __init__(self, stopPointName, stopid, stopcode1, latitude, longitude,
                 lineName, directionid, destination, estimatedTime):
        self.stopid = stopid
        self.stopcode1 = stopcode1
        self.stopPointName = stopPointName
        self.latitude = latitude
        self.longitude = longitude
        self.lineName = lineName
        self.directionid = directionid
        self.destination = destination
        diff = datetime.fromtimestamp(int(
                                      estimatedTime / 1000)) - datetime.now()
        self.estimatedTime = diff.days * 86400 + diff.seconds

    def __str__(self):
        return str(self.__dict__)


class BusLine(object):
    def __init__(self, lineName, stopPointName, directionid, destination):
        self.lineName = lineName
        self.stopPointName = stopPointName
        self.directionid = directionid
        self.destination = destination
        self.estimatedTimeInSeconds = []

    def putArrivalTimes(self, estimatedTime):
        self.estimatedTimeInSeconds.append(estimatedTime)
        self.estimatedTimeInSeconds.sort()

    def __str__(self):
        return str(self.__dict__)


class Stop(object):
    def __init__(self, stopid, stopcode1, latitude, longitude):
        self.stopid = stopid
        self.stopcode1 = stopcode1
        self.latitude = latitude
        self.longitude = longitude
        self.lines = []

    def putLine(self, line):
        existingLines = map(lambda x: x.lineName, self.lines)
        if line.lineName in existingLines:
            for l in self.lines:
                if l.lineName == line.lineName:
                    l.putArrivalTimes(line.estimatedTimeInSeconds[0])
                    break
        else:
            self.lines.append(line)
            self.lines.sort()

    def __str__(self):
        return str(self.__dict__)

