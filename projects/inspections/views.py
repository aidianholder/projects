from django.shortcuts import render
from django.http import HttpResponse


from .models import Facility
from .models import Inspections

# Create your views here.

def index(request):
    return HttpResponse("index page will go here index page will go here")

def city(request, lookup_city):
    city_facilities = Facility.objects.filter(city=lookup_city)
    context = {'facilities': city_facilities, 'city': city}
    return render(request, 'inspections/city.html', context)

def facility(request, facility_uuid):
    restaurant = Facility.objects.get(guid=facility_uuid)
    all_inspections = restaurant.inspections_set.all()
    pass_fail_stats = restaurant.pass_fail_total()
    latest = restaurant.latest_inspection()
    context = {'facility':restaurant,'inspections':all_inspections,'stats':pass_fail_stats,'latest':latest}
    return render(request, 'inspections/facility_detail.html', context)

def inspection_detail(request, inspection_identifier):
    details = Inspections.objects.get(id=inspection_identifier)
    context = {'type':details.inspection_type, 'date': details.inspection_date, 'critical': details.critical_points, 'total': details.total_points, 'notes': details.inspection_details}
    return render(request, 'inspections/inspections_detail.html', context)
