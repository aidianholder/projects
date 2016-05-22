from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from arcgis import ArcGIS
from ...models import Calls
import datetime
from django.contrib.gis.geos import GEOSGeometry


class Command(NoArgsCommand):
    help = 'downloads calls for service from YPD for yesterday and loads them into database as Calls objects'

    def handle(self, *args, **options):
        source = "https://gis.yakimawa.gov/arcgis101/rest/services/CouncilDistricts/Analysis/MapServer"
        service = ArcGIS(source)
        yesterday = datetime.date.today() - datetime.timedelta(1)
        yday = yesterday.strftime("%m/%d/%Y")
        geojson = service.get(0, where="CallDate = '%(yday)s'" % {'yday': yday})
        calls_list = geojson['features']
        feature_count = 0
        for call in calls_list:
            g = call['geometry']['coordinates']
            p = call['properties']
            c = Calls()
            c.lat, c.lon = g[0], g[1]
            c.geom = GEOSGeometry('POINT({:.6f} {:.6f})'.format(c.lat, c.lon), srid=4326)
            c.callid = int(p['CallID'])
            c.nature = p['Nature'].strip()
            c.callcategory = p['CallCategory'].strip()
            c.address = p['Address'].strip()
            c.calldatetime = datetime.datetime.fromtimestamp(p['CallDateTime'] / 1000)
            c.save()
            feature_count += 1
        self.stdout.write('processed {} features'.format(feature_count))


#outfile = open('/Users/admin/src/projects/projects/crimemap/data/yday_calls.geojson', 'w')
#outfile.write(geojson.read())
#outfile.close()


