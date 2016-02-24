from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^city/(?P<city>\[a-zA-Z]+)/$', views.city, name="city"),
    url(r'^facility/(?P<city>\D+)/(?P<facility>/[\w\s]+)/$', views.facility, name='facility_detail' ),
    url(r'^inspection/(?P<city>\D+)/(?P<facility>/[\w\s]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.inspection_detail, name='inspection_detail'),
]


