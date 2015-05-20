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
    route = models.CharField(max_length=64, db_index=True)
    run = models.IntegerField(db_index=True)
    sequence = models.IntegerField(db_index=True)
    stop_code_lbsl = models.CharField(max_length=64)
    bus_stop_code = models.CharField(max_length=64)
    naptan_atco = models.CharField(max_length=64, db_index=True)
    stop_name = models.CharField(max_length=64)
    location_easting = models.IntegerField()
    location_northing = models.IntegerField()
    heading = models.IntegerField()
    virtual_bus_stop = models.IntegerField()
    average_travel_time = models.DecimalField(max_digits=11, decimal_places=1,
                                              default=0.0)
    cumulative_travel_time = models.DecimalField(max_digits=11,
                                                 decimal_places=1,
                                                 default=0.0)
    curr_average_travel_time = models.DecimalField(max_digits=11,
                                                   decimal_places=1,
                                                   default=0.0)
    curr_cumulative_travel_time = models.DecimalField(max_digits=11,
                                                      decimal_places=1,
                                                      default=0.0)

    def __str__(self):
        return str(self.__dict__)


class Current_timetable(models.Model):
    start_stop = models.CharField(max_length=64, db_index=True)
    end_stop = models.CharField(max_length=64, db_index=True)
    average_travel_time = models.DecimalField(max_digits=11, decimal_places=1,
                                              default=0.0)

    def __str__(self):
        return str(self.__dict__)


class Tfl_timetable(models.Model):
    route = models.CharField(max_length=16, db_index=True)
    day = models.CharField(max_length=32, db_index=True)
    run = models.IntegerField(db_index=True)
    sequence = models.IntegerField(db_index=True)
    naptan_atco = models.CharField(max_length=64, default='', db_index=True)
    stop_name = models.CharField(max_length=64)
    departure_time_from_origin = models.DateTimeField(db_index=True)
    arrival_time = models.DateTimeField(db_index=True)
    travel_time = models.IntegerField()
    cumulative_travel_time = models.IntegerField()


class Arrival(object):

    def __init__(self, stop_name, stop_code_lbsl, sms_code, naptan_atco,
                 latitude, longitude, route, run, destination, estimatedTime):
        self.stop_code_lbsl = stop_code_lbsl
        self.sms_code = sms_code
        self.naptan_atco = naptan_atco
        self.stop_name = stop_name
        self.latitude = latitude
        self.longitude = longitude
        self.route = route
        self.run = run
        self.destination = destination
        diff = datetime.fromtimestamp(int(
                                      estimatedTime / 1000)) - datetime.now()
        self.estimatedTime = diff.days * 86400 + diff.seconds

    def __str__(self):
        return str(self.__dict__)


class BusLine(object):
    def __init__(self, route, stop_name, run, destination):
        self.route = route
        self.stop_name = stop_name
        self.run = run
        self.destination = destination
        self.estimatedTimeInSeconds = []

    def putArrivalTimes(self, estimatedTime):
        self.estimatedTimeInSeconds.append(estimatedTime)
        self.estimatedTimeInSeconds.sort()

    def __str__(self):
        return str(self.__dict__)


class Stop(object):
    def __init__(self, stop_code_lbsl, sms_code, naptan_atco,
                 latitude, longitude):
        self.stop_code_lbsl = stop_code_lbsl
        self.sms_code = sms_code
        self.naptan_atco = naptan_atco
        self.latitude = latitude
        self.longitude = longitude
        self.lines = []

    def putLine(self, line):
        existingLines = map(lambda x: x.route, self.lines)
        if line.route in existingLines:
            for l in self.lines:
                if l.route == line.route:
                    l.putArrivalTimes(line.estimatedTimeInSeconds[0])
                    break
        else:
            self.lines.append(line)
            self.lines.sort(key=lambda line: line.route)

    def __str__(self):
        return str(self.__dict__)

