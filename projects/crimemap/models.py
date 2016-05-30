from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime


@python_2_unicode_compatible
class Calls(models.Model):
    callid = models.IntegerField(primary_key=True)
    nature = models.CharField(max_length=16)
    callcategory = models.CharField(max_length=50)
    callgroup = models.CharField(max_length=2)
    address = models.CharField(max_length=61)
    calldatetime = models.DateTimeField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    geom = models.PointField(srid=3857)

    def __str__(self):
        return "%s %s %s" % (self.nature, self.calldatetime, self.address)
