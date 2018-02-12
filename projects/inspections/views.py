from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse

import json

from .models import Facility
from .models import Inspections


def index(request):
    return HttpResponse("index page will go here index page will go here")


def city(request, lookup_city):
    city_facilities = Facility.objects.filter(city=lookup_city)
    context = {'facilities': city_facilities, 'city': lookup_city}
    return render(request, 'inspections/city.html', context)


def facility(request, facility_uuid):
    restaurant = Facility.objects.get(guid=facility_uuid)
    all_inspections = restaurant.inspections_set.all()
    pass_fail_stats = restaurant.pass_fail_total()
    number_passed = pass_fail_stats['passed']
    number_failed = pass_fail_stats['failed']
    percent_passed = pass_fail_stats['passed_percent']
    latest = restaurant.latest_inspection()
    context = {'facility':restaurant,'inspections':all_inspections, 'passed':number_passed, 'failed': number_failed, 'percent_passed': percent_passed,'latest':latest}
    return render(request, 'inspections/facility_detail.html', context)


def inspection_detail(request, id):
    details = Inspections.objects.get(id=id)
    context = {'type':details.inspection_type, 'date': details.inspection_date, 'critical': details.critical_points, 'total': details.total_points, 'notes': details.inspection_details}
    return render(request, 'inspections/inspections_detail.html', context)


def cityjsonp(request, l_city):
    city_facilities = Facility.objects.filter(city=l_city)
    facilities_data = []
    for establishment in city_facilities:
        restaurant = dict()
        restaurant["name"] = establishment.facility_name
        restaurant["type"] = establishment.facility_type
        restaurant["address"] = establishment.address
        restaurant["city"] = establishment.city
        restaurant["id"] = str(establishment.guid)
        restaurant["latest"] = establishment.latest_inspection().strftime('%m/%d/%Y')

        facilities_data.append(restaurant)
    json_data = json.dumps(facilities_data)
    data = '%s(%s)' % (request.GET.get('callback'), json_data)
    return HttpResponse(data, "text/javascript")


def alljsonp(request):
    facilities = Facility.objects.all()
    facilities_data = []
    for establishment in facilities:
        restaurant = dict()
        restaurant["name"] = establishment.facility_name
        restaurant["type"] = establishment.facility_type
        restaurant["address"] = establishment.address
        restaurant["city"] = establishment.city
        restaurant["id"] = str(establishment.guid)
        restaurant["latest"] = establishment.latest_inspection().strftime('%m/%d/%Y')
	pftotals = establishment.pass_fail_total()
	restaurant["passed"] = int(pftotals['passed'])
	restaurant["failed"] = int(pftotals['failed']) 	
        facilities_data.append(restaurant)
    json_data = json.dumps(facilities_data)
    data = '%s(%s)' % (request.GET.get('callback'), json_data)
    return HttpResponse(data, "text/javascript")


def facilityjsonp(request, facility_uuid):
    facility = Facility.objects.get(guid=facility_uuid)
    inspections_performed = Inspections.objects.filter(facility_guid_id = facility_uuid)
    facility_details = dict()
    facility_details["name"] = facility.facility_name
    facility_details["type"] = facility.facility_type
    facility_details["address"] = facility.address
    facility_details["city"] = facility.city
    pftotals = facility.pass_fail_total()
    facility_details["pass"] = int(pftotals['passed'])
    facility_details["fail"] = int(pftotals['failed'])
    inspections = []
    for inspection in inspections_performed:
        record = dict()
        record["date"] = inspection.inspection_date.strftime("%x")
        record["type"] = inspection.inspection_type
        record["critical"] = inspection.critical_points
        record["total"] = inspection.total_points
        record["notes"] = inspection.inspection_details
        record["pf"] = inspection.passed_or_failed()
        inspections.append(record)
    data_object = {"facility": facility_details, "inspections": inspections}
    json_data = json.dumps(data_object)
    json_data.replace("\n", " ")
    data = '%s(%s)' % (request.GET.get('callback'), json_data)
    return HttpResponse(data, "text/javascript")

    #inspection_record["inspections"] = []

#json_data = serializers.serialize('json', city_facilities, fields=('facility_name', 'facility_type', 'city', 'address', 'guid'))
    #callback = 'myFunc'

    #return JsonResponse('%s(%s)' % (request.GET.get('callback'), facilities_data), safe=False)
