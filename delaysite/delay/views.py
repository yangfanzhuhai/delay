from django.shortcuts import render
from delay.models import Neighbours, Bus_sequences, Timetable
from rest_framework import viewsets
from delay.serializers import PredictionsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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


def index(request):
    neighbours_list = Neighbours.objects.all()
    context = {'neighbours_list': neighbours_list}
    # render(request object, template name, dictionary)
    return render(request, 'delay/index.html', context)
