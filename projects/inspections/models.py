from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Facility(models.Model):
    facility_name = models.CharField(max_length=100)
    facility_type = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return "%s %s" % (self.facility_name, self.city)

    class Meta:
        unique_together = ("facility_name", "facility_type", "address", "city")

@python_2_unicode_compatible
class Inspections(models.Model):
    facility = models.ForeignKey('Facility', on_delete=models.CASCADE)
    inspection_type = models.CharField(max_length=50)
    inspection_date = models.DateField()
    critical_points = models.IntegerField()
    total_points = models.IntegerField()
    inspection_details = models.TextField()

    def __str__(self):
        return "%s %s %s" % (self.facility, self.inspection_date, self.inspection_type)

    def passed_or_failed(self):
        if int(self.total_points) > 40 or int(self.critical_points) > 35:
            return 'failed'
        else:
            return 'passed'



