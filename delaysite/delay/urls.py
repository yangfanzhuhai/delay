from django.conf.urls import patterns, url

from delay import views

urlpatterns = patterns('',
                       # ex: /delay/
                       url(r'^$', views.index, name='index'),
                       # ex: /delay/1/
                       url(r'^(?P<neighbours_id>\d+)/$',
                           views.neighbours, name='neighbours'),
                       # ex: /polls/1/timetable/
                       url(r'^(?P<neighbours_id>\d+)/timetable/$',
                           views.timetable, name='timetable'),
                       # ex: /polls/1/timetable/
                       url(r'^route/(?P<route_name>\d+)/' +
                           'run/(?P<run_id>\d+)/' +
                           'day/(?P<day_of_week>\w+)/' +
                           'hour/(?P<h>\w+)/$',
                           views.sequence, name='sequence'),
                       )
