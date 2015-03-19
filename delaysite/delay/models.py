from django.db import models


class Neighbours(models.Model):
    route = models.CharField(max_length=64)
    start_stop = models.CharField(max_length=64)
    end_stop = models.CharField(max_length=64)

    def __str__(self):
        return str(self.__dict__)

        # return 'route: {}, start_stop: {}, end_stop: {}'.format
        # (self.route, self.start_stop, self.end_stop)


class Timetable(models.Model):
    start_stop = models.CharField(max_length=64)
    end_stop = models.CharField(max_length=64)
    day = models.CharField(max_length=9)
    hour = models.IntegerField()
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

    def __str__(self):
        return "route: {}, run: {}, sequence: {}, stop_code_lbsl:".format
        (self.route, self.run, self.sequence, self.stop_code_lbsl)
