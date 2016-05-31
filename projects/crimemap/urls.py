from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<callgroups>[A-Z]+)/$', views.incidents),
    url(r'(?P<callgroups>[A-Z]+)/(?P<days>[0-9]+)/$', views.incidents),
]
