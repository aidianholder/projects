from django.http import HttpResponse
from django.core.serializers import serialize
from django.db.models import Q

import datetime
from operator import __or__ as OR

from .models import Calls


def incidents(request, callgroups, days="1"):
    tday = datetime.datetime.today()
    y, m, d = tday.year, tday.month, tday.day
    start_day = datetime.datetime(y, m, d) - datetime.timedelta(int(days))
    cgn = len(callgroups) / 2
    groups = []
    ls, rs = 0, 2
    for i in range(0, cgn):
        cg = callgroups[ls:rs]
        groups.append(cg)
        ls = rs
        rs += 2
    if len(groups) == 1:
        service_calls = Calls.objects.filter(calldatetime__gte=start_day).filter(callgroup=groups[0])
    elif len(groups) > 1:
        service_calls = Calls.objects.filter(calldatetime__gte=start_day)
        qlist = []
        for group in groups:
            q = Q(callgroup=group)
            qlist.append(q)
        service_calls = service_calls.filter(reduce(OR, qlist))
    data = serialize('geojson', service_calls, srid=4326)
    return HttpResponse(data, content_type='application/json')
