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


class Arrival(object):
    def __init__(self, stopPointName, latitude, longitude,
                 lineName, estimatedTime):
        self.stopPointName = stopPointName
        self.latitude = latitude
        self.longitude = longitude
        self.lineName = lineName
        self.estimatedTime = datetime.fromtimestamp(int(estimatedTime / 1000))

    def __str__(self):
        return str(self.__dict__)
