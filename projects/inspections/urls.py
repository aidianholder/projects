from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^city/(?P<lookup_city>\D+)/$', views.city, name="city"),
    url(r'^facility/(?P<facility_uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/$', views.facility, name='facility_detail'),
    url(r'^inspection/(?P<id>\d+)/$', views.inspection_detail, name='inspection_detail'),
]


