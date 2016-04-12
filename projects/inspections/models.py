from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from decimal import *
import uuid


@python_2_unicode_compatible
class Facility(models.Model):
    facility_name = models.CharField(max_length=100)
    facility_type = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    guid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)

    def __str__(self):
        return "%s %s" % (self.facility_name, self.city)

    def pass_fail_total(self):
        all_inspections = self.inspections_set.all()
        passed = Decimal(0)
        failed = Decimal(0)
        for event in all_inspections:
            if event.passed_or_failed() == 'passed':
                passed += 1
            if event.passed_or_failed() == 'failed':
                failed += 1
        failed_percent = 100 * (Decimal(failed)/Decimal(failed + passed))
        passed_percent = Decimal(100) - failed_percent
        return {'failed': failed, 'passed': passed, 'failed_percent': failed_percent, 'passed_percent': passed_percent}

    def latest_inspection(self):
        most_recent = self.inspections_set.latest('inspection_date')
        return most_recent.inspection_date

    class Meta:
        #unique_together = ("facility_name", "facility_type", "address", "city")
        verbose_name_plural = "Facilities"


@python_2_unicode_compatible
class Inspections(models.Model):
    facility_guid = models.ForeignKey(Facility, on_delete=models.CASCADE)
    inspection_type = models.CharField(max_length=50)
    inspection_date = models.DateField()
    critical_points = models.IntegerField()
    total_points = models.IntegerField()
    inspection_details = models.TextField()

    def __str__(self):
        return "%s %s %s" % (self.facility_guid.facility_name, self.inspection_date, self.inspection_type)

    def passed_or_failed(self):
        if int(self.total_points) > 40 or int(self.critical_points) > 35:
            return 'failed'
        else:
            return 'passed'

    class Meta:
        ordering = ['-inspection_date']
        verbose_name_plural = "Inspections"



