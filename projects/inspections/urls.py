from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^city/(?P<city>\D+)/$', views.city, name="city"),
    url(r'^facility/(?P<facility>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}/$', views.facility, name='facility_detail'),
    url(r'^inspection/(?P<city>D+)/(?P<facility>/[\w\s]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.inspection_detail, name='inspection_detail'),
]


