from django.shortcuts import render
from delay.models import Bus_sequences, Timetable, Arrival
from rest_framework import viewsets
from delay.serializers import PredictionsSerializer, ArrivalsSerializer
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
    serializer_class = PredictionsSerializer
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


def get_arrivals(latitude, longitude, radius):
    url = ('http://countdown.api.tfl.gov.uk/interfaces/ura/'
           'instant_V1?Circle={},{},{}'
           '&ReturnList=StopPointName,Latitude,'
           'Longitude,LineName,EstimatedTime#').format(
           latitude, longitude, radius)

    r = requests.get(
        url,
        auth=('LiveBus95085', 'rU9HUx4ZEm')
    )

    output = []
    for line in r.iter_lines():
        if not line:
            continue
        line = json.loads(line.decode('utf-8-sig'))
        if line[0] != 1:
            continue
        line = line[1:]
        arrival = Arrival(*line)
        output.append(arrival)
        stops = set(map(lambda x: x.stopPointName, output))
        groups = [[y for y in output if y.stopPointName == x] for x in stops]
    return groups


class ArrivalsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        latitude = self.request.QUERY_PARAMS.get('latitude', None)
        longitude = self.request.QUERY_PARAMS.get('longitude', None)
        radius = self.request.QUERY_PARAMS.get('radius', 200)
        output = get_arrivals(latitude, longitude, radius)
        result = [ArrivalsSerializer(queryset, many=True).data
                  for queryset in output]
        return Response(result)

