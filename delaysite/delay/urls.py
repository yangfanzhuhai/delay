from django.conf.urls import patterns, url, include
from delay import views


# ex: /delay/route/9/run/1/day/Monday/hour/3/
delay_urls = patterns('',
                      url(r'^/(?P<route_name>\d+)/' +
                          'run/(?P<run_id>\d+)/' +
                          'day/(?P<day>\w+)/' +
                          'hour/(?P<hour>\w+)/$',
                          views.sequence, name='sequence')
                      )

urlpatterns = patterns('',
                       url(r'^$', views.get_arrivals, name='index'),
                       url(r'^route', include(delay_urls)),
                       )
