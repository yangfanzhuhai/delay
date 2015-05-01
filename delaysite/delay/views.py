from django.shortcuts import render
from delay.models import Bus_sequences, Timetable, Arrival, BusLine, Stop
from rest_framework import viewsets
import delay.serializers as s
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import requests
import json


def get_travel_time(bus_sequences, day, hour):
    for current, nxt in zip(bus_sequences, bus_sequences[1:]):
        current_stop = current.stop_code_lbsl
        nxt_stop = nxt.stop_code_lbsl
        timetable_object = Timetable.objects.filter(
            start_stop=current_stop, end_stop=nxt_stop, day=day, hour=hour)

        bus_sequences[current.sequence].average_travel_time = float(
                     list(timetable_object)[0].average_travel_time)
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
           '&ReturnList=StopPointName,Latitude,'
           'Longitude,LineName,EstimatedTime#').format(
           latitude, longitude, radius)
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
            busLine = BusLine(lineName=arrival.lineName)
            busLine.putArrivalTimes(arrival.estimatedTime)
            if arrival.stopPointName in groups:
                groups[arrival.stopPointName].putLine(busLine)
            else:
                stop = Stop(arrival.stopPointName, arrival.latitude,
                            arrival.longitude)
                stop.putLine(line=busLine)
                groups[arrival.stopPointName] = stop
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

