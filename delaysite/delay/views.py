from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
# from django.template import RequestContext, loader

from delay.models import Neighbours, Bus_sequences, Timetable


def index(request):
    neighbours_list = Neighbours.objects.all()
    context = {'neighbours_list': neighbours_list}
    # render(request object, template name, dictionary)
    return render(request, 'delay/index.html', context)


def neighbours(request, neighbours_id):
    # return HttpResponse("You're looking at neighbours %s." % neighbours_id)
    try:
        neighbours = Neighbours.objects.get(pk=neighbours_id)
    except Neighbours.DoesNotExist:
        raise Http404("Neighbours does not exist")
    return render(request, 'delay/detail.html', {'neighbours': neighbours})


def timetable(request, neighbours_id):
    response = "You're looking at the timetable entry of neighbours %s."
    return HttpResponse(response % neighbours_id)


def sequence(request, run_id, route_name, day_of_week, h):
    bus_sequences = Bus_sequences.objects.filter(route=route_name, run=run_id)
    travel_time = [0]

    for current, nxt in zip(bus_sequences, bus_sequences[1:]):
        current_stop = current.stop_code_lbsl
        nxt_stop = nxt.stop_code_lbsl
        timetable_object = Timetable.objects.filter(start_stop=current_stop,
                                                    end_stop=nxt_stop,
                                                    day=day_of_week,
                                                    hour=h)
        if timetable_object:
            travel_time.append(float(list(timetable_object)[0].
                               average_travel_time))
        else:
            travel_time.append(0.0)
    bus_sequences = zip(bus_sequences, travel_time)
    context = {'bus_sequences': bus_sequences,
               'day_of_week': day_of_week,
               'h': h,
               'travel_time': travel_time}
    # render(request object, template name, dictionary)
    return render(request, 'delay/sequence.html', context)
