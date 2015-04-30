from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from delay import views


router = routers.DefaultRouter()
router.register(r'predictions', views.PredictionsViewSet,
                base_name='predictions')
router.register(r'arrivals', views.ArrivalsViewSet,
                base_name='arrivals')


urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
                       url(r'^delay/', include('delay.urls')),

                       url(r'^admin/', include(admin.site.urls))
                       )

