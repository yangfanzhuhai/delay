from django.shortcuts import render
from delay.models import Bus_sequences, Timetable, Arrival, BusLine, Stop
from delay.models import Tfl_timetable
from rest_framework import viewsets
import delay.serializers as s
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import requests
import json
import datetime as dt


def get_travel_time(bus_sequences, day, hour):
    for current, nxt in zip(bus_sequences, bus_sequences[1:]):
        current_stop = current.stop_code_lbsl
        nxt_stop = nxt.stop_code_lbsl
        timetable_object = Timetable.objects.filter(
            start_stop=current_stop, end_stop=nxt_stop, day=day, hour=hour)
        avg = None
        if timetable_object:
            avg = float(list(timetable_object)[0].average_travel_time)
        bus_sequences[current.sequence].average_travel_time = avg
    return bus_sequences


class PredictionsViewSet(viewsets.ModelViewSet):
    serializer_class = s.PredictionsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Bus_sequences.objects.all()
        route = self.request.QUERY_PARAMS.get('route', None)
        run = self.request.QUERY_PARAMS.get('run', None)
        day = self.request.QUERY_PARAMS.get('day', None)
        hour = self.request.QUERY_PARAMS.get('hour', None)
        if route is not None:
            queryset = queryset.filter(route=route)
        if route is not None:
            queryset = queryset.filter(run=run)

        return get_travel_time(queryset, day, hour)


def getTflTimetableEntries(queryset, day, naptan_atco):
    if day is not None:
        dbDays = list(queryset.values_list('day', flat=True).distinct())
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if day in dbDays:
            queryset = queryset.filter(day=day)
        elif day in weekdays:
            queryset = queryset.filter(day='MondayToFriday')
        else:
            queryset = queryset.filter(day='Weekend')
    if naptan_atco is not None:
        currentStop = queryset.filter(naptan_atco=naptan_atco)
        currentSeq = currentStop.values_list('sequence', flat=True)
        if currentSeq:
            departureTimes = queryset.values_list('departure_time_from_origin',
                                                  flat=True).distinct()
            ordered = departureTimes.order_by('departure_time_from_origin')
            earliestTime = list(ordered)[0]
            baseSequence = currentSeq[0]
            queryset = queryset.filter(sequence__gte=baseSequence,
                                       departure_time_from_origin=earliestTime)
    return queryset


class TflTimetableViewSet(viewsets.ModelViewSet):
    serializer_class = s.TflTimetableSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Tfl_timetable.objects.all()
        route = self.request.QUERY_PARAMS.get('route', None)
        run = self.request.QUERY_PARAMS.get('run', None)
        day = self.request.QUERY_PARAMS.get('day', None)
        hour = self.request.QUERY_PARAMS.get('hour', None)
        naptan_atco = self.request.QUERY_PARAMS.get('naptan_atco', None)
        if route is not None:
            queryset = queryset.filter(linename=route)
        if run is not None:
            queryset = queryset.filter(run=run)
        if hour is not None:
            currentTime = dt.datetime.strptime(hour, '%H:%M:%S').time()
            currentDate = dt.datetime.combine(dt.date(2015, 1, 1), currentTime)
            queryset = queryset.filter(arrival_time__gt=currentDate)

        return getTflTimetableEntries(queryset, day, naptan_atco)


def sequence(request, run_id, route_name, day, hour):
    bus_sequences = Bus_sequences.objects.filter(route=route_name, run=run_id)
    bus_sequences = get_travel_time(bus_sequences, day, hour)
    context = {'bus_sequences': bus_sequences,
               'day': day,
               'hour': hour}
    # render(request object, template name, dictionary)
    return render(request, 'delay/sequence.html', context)


def get_countdown_response(latitude, longitude, radius):
    url = ('http://countdown.api.tfl.gov.uk/interfaces/ura/'
           'instant_V1?Circle={},{},{}'
           '&ReturnList=StopID,StopCode1,StopPointName,Latitude,'
           'Longitude,LineName,DirectionID,DestinationName,'
           'EstimatedTime#').format(latitude, longitude, radius)
    r = requests.get(
        url,
        auth=('LiveBus95085', 'rU9HUx4ZEm')
    )
    return r


def process_countdown_info(r):
    result = []
    for line in r.iter_lines():
        if not line:
            continue
        line = json.loads(line.decode('utf-8-sig'))
        if line[0] != 1:
            continue
        line = line[1:]
        result.append(line)
    return result


def get_arrivals(latitude, longitude, radius):
    r = get_countdown_response(latitude, longitude, radius)
    if r.status_code == 200:
        lines = process_countdown_info(r)
        groups = {}
        for line in lines:
            arrival = Arrival(*line)
            busLine = BusLine(arrival.lineName,
                              arrival.stopPointName,
                              arrival.directionid,
                              arrival.destination)
            busLine.putArrivalTimes(arrival.estimatedTime)
            if arrival.stopcode1 in groups:
                groups[arrival.stopcode1].putLine(busLine)
            else:
                stop = Stop(arrival.stopid,
                            arrival.stopcode1,
                            arrival.latitude,
                            arrival.longitude)
                stop.putLine(line=busLine)
                groups[arrival.stopcode1] = stop
        return list(groups.values())


class ArrivalsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        latitude = self.request.QUERY_PARAMS.get('latitude', None)
        longitude = self.request.QUERY_PARAMS.get('longitude', None)
        radius = self.request.QUERY_PARAMS.get('radius', 200)
        output = get_arrivals(latitude, longitude, radius)
        serializer = s.StopSerializer(output, many=True)
        return Response(serializer.data)

