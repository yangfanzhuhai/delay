from django.conf.urls import patterns, url
from delay import views

urlpatterns = patterns('',
                       # ex: /delay/
                       url(r'^$', views.index, name='index'),
                       # ex: /delay/route/9/run/1/day/Monday/hour/3/
                       url(r'^route/(?P<route_name>\d+)/' +
                           'run/(?P<run_id>\d+)/' +
                           'day/(?P<day>\w+)/' +
                           'hour/(?P<hour>\w+)/$',
                           views.sequence, name='sequence')
                       )
