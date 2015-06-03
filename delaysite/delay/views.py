from django.shortcuts import render
from delay.models import Bus_sequences, Timetable, Arrival, BusLine, Stop
from delay.models import Tfl_timetable, Current_timetable
from rest_framework import viewsets
import delay.serializers as s
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import requests
import json
import datetime as dt


def get_travel_time(bus_sequences, day, hour, baseSequence):
    bus_sequences = bus_sequences.order_by('sequence')
    cumulative_travel_time = 0.0
    curr_cumu = 0.0
    historical = Timetable.objects.filter(day=day, hour=hour)
    for current, nxt in zip(bus_sequences, bus_sequences[1:]):
        current_stop = current.stop_code_lbsl
        nxt_stop = nxt.stop_code_lbsl
        timetable_object = historical.filter(start_stop=current_stop,
                                             end_stop=nxt_stop)
        avg = 0.0

        index = current.sequence - baseSequence + 1
        if timetable_object.exists():
            avg = float(timetable_object.values()[0]['average_travel_time'])
        bus_sequences[index].average_travel_time = avg
        cumulative_travel_time += avg
        bus_sequences[index].cumulative_travel_time = cumulative_travel_time

        curr_avg = 0.0

        current_timetable_object = Current_timetable.objects.filter(
               start_stop=current_stop, end_stop=nxt_stop)
        if current_timetable_object.exists():
            curr_avg = float(current_timetable_object.values()[0]
                             ['average_travel_time'])
        bus_sequences[index].curr_average_travel_time = curr_avg
        curr_cumu += curr_avg
        bus_sequences[index].curr_cumulative_travel_time = curr_cumu

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
        naptan_atco = self.request.QUERY_PARAMS.get('naptan_atco', None)
        if route is not None:
            queryset = queryset.filter(route=route)
        if route is not None:
            queryset = queryset.filter(run=run)
        baseSequence = 1
        if naptan_atco is not None:
            currentStop = queryset.filter(naptan_atco=naptan_atco)
            currentSeq = currentStop.values_list('sequence', flat=True)
            if currentSeq:
                baseSequence = currentSeq[0]
                queryset = queryset.filter(sequence__gte=baseSequence)
        return get_travel_time(queryset, day, hour, baseSequence)


def getTflTimetableEntries(queryset, day, naptan_atco, sequence):
    if day is not None:
        dbDays = list(queryset.values_list('day', flat=True).distinct())
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if day in dbDays:
            queryset = queryset.filter(day=day)
        elif day in weekdays:
            if 'MondayToFriday' in dbDays:
                queryset = queryset.filter(day='MondayToFriday')
            else:
                queryset = queryset.filter(day='Monday')
        else:
            queryset = queryset.filter(day='Weekend')

    baseSequence = 1
    if sequence is not None:
        baseSequence = sequence
    elif naptan_atco is not None:
        currentStop = queryset.filter(naptan_atco=naptan_atco)
        currentSeq = currentStop.values_list('sequence', flat=True)
        if currentSeq:
            baseSequence = currentSeq[0]

    queryset = queryset.filter(sequence__gte=baseSequence).order_by('sequence')
    baseTravelTime = queryset[0].cumulative_travel_time
    for entry in queryset:
        entry.cumulative_travel_time = entry.cumulative_travel_time - baseTravelTime
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
        sequence = self.request.QUERY_PARAMS.get('sequence', None)
        if route is not None:
            queryset = queryset.filter(route=route)
        if run is not None:
            queryset = queryset.filter(run=run)
        if hour is not None:
            queryset = queryset.filter(arrival_hour=hour)

        return getTflTimetableEntries(queryset, day, naptan_atco, sequence)


def sequence(request, run_id, route_name, day, hour):
    bus_sequences = Bus_sequences.objects.filter(route=route_name, run=run_id)
    bus_sequences = get_travel_time(bus_sequences, day, hour, 1)
    context = {'bus_sequences': bus_sequences,
               'day': day,
               'hour': hour}
    # render(request object, template name, dictionary)
    return render(request, 'delay/sequence.html', context)


def get_countdown_response(latitude, longitude, radius):
    url = ('http://countdown.api.tfl.gov.uk/interfaces/ura/'
           'instant_V1?Circle={},{},{}'
           '&ReturnList=StopID,StopCode1,StopCode2,StopPointName,Latitude,'
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
    existingLines = set()

    if r.status_code == 200:
        lines = process_countdown_info(r)
        groups = {}
        for line in lines:
            arrival = Arrival(*line)
            busLine = BusLine(arrival.route,
                              arrival.stop_name,
                              arrival.run,
                              arrival.destination)
            busLine.putArrivalTimes(arrival.estimatedTime)
            if (arrival.route, arrival.destination) not in existingLines:
                existingLines.add((arrival.route, arrival.destination))
                if arrival.sms_code in groups:
                    groups[arrival.sms_code].putLine(busLine)
                else:
                    stop = Stop(arrival.stop_code_lbsl,
                                arrival.sms_code,
                                arrival.naptan_atco,
                                arrival.latitude,
                                arrival.longitude)
                    stop.putLine(line=busLine)
                    groups[arrival.sms_code] = stop
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

