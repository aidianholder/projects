from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from arcgis import ArcGIS
from ...models import Calls
import datetime
import os
from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'downloads calls for service from YPD for yesterday and loads them into database as Calls objects'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, help="select day to download as number of days before today. Default is 1, scraping too many means you won't get all the calls")

    def handle(self, *args, **options):
        source = "https://gis.yakimawa.gov/arcgis101/rest/services/CouncilDistricts/Analysis/MapServer"
        service = ArcGIS(source)
        if options['days']:
            target_day = datetime.date.today() - datetime.timedelta(options['days'])
        else:
            target_day = datetime.date.today() - datetime.timedelta(1)
        tday = target_day.strftime("%m/%d/%Y")
        json_raw = service.get(0, where="CallDate = '%(tday)s'" % {'tday': tday})
        calls_list = json_raw['features']
        feature_count = 0
        lookup = {
            "ACCIDENT HITRUN": "TR",
            "ACCIDENT INJURY": "TR",
            "ACCIDENT NO INJ": "TR",
            "ACCIDENT UNKNOW": "TR",
            "ASSAULT WEAPON": "VI",
            "CIVIL MATTER": "CV",
            "COURT ORDER SER": "CV",
            "COURT ORDER VIO": "CV",
            "DOMESTIC": "DM",
            "DRUGS": "DR",
            "OVERDOSE": "DR",
            "DUI": "DR",
            "CUSTODIAL INTER": "DM",
            "MENTAL SUBJECT": "OT",
            "SUICIDAL PERSON": "OT",
            "NOISE COMPLAINT": "OT",
            "TRESPASSING": "PR",
            "UNWANTED GUEST": "OT",
            "ILLEGAL DUMPING": "OT",
            "ABUSE NEGLECT": "DM",
            "AGENCY ASSIST": "OT",
            "ATMT TO LOCATE": "OT",
            "CITIZEN ASSIST": "CV",
            "CITIZEN DISPUTE": "CV",
            "CITIZEN COMPLAI": "CV",
            "FIREWORKS": "OT",
            "FOUND PROPERTY": "PR",
            "INFORMATION": "OT",
            "MISSING PERSON": "OT",
            "TRANSPORT": "OT",
            "WARRANT SERVICE": "OT",
            "BURGLARY": "PR",
            "RECOVRD STOLEN": "PR",
            "THEFT": "PR",
            "THEFT-VEHICLE": "PR",
            "VEHICLE PROWL": "PR",
            "MAL MISCHIEF": "PR",
            "FRAUD": "PR",
            "SUSPICIOUS CIRC": "SC",
            "PROWLER": "PR",
            "HARASSMENT": "VI",
            "THREATS": "VI",
            "PARKING PROBLEM": "TR",
            "TRAFFIC HAZARD": "TR",
            "TRAFFIC OFFENSE": "TR",
            "TRAFFIC STOP": "TR",
            "ASSAULT": "VI",
            "DEATH INVEST": "VI",
            "ROBBERY": "VI",
            "SHOTS FIRED": "VI",
            "WEAPON OFFENSE": "VI",
            "WANTED PERSON": "OT",
            "ABANDONED VEHIC": "OT",
            "LOST PROPERTY": "PR",
            "INDUSTRIAL ACC": "OT"
        }
        call_natures = []

        """propertycrime = ['BURGLARY', 'THEFT', 'THEFT-VEHICLE', 'VEHICLE PROWL', 'MAL MISCHIEF', 'RECOVERD STOLEN']
        violence = ['ASSAULT', 'DEATH INVEST', 'ROBBERY', 'SHOTS FIRED', 'WEAPON OFFENSE']
        accident = ['ACCIDENT HITRUN', 'ACCIDENT INJURY', 'ACCIDENT NO INJ', 'ACCIDENT UNKOW']
        traffic = ['PARKING PROBLEM', 'TRAFFIC HAZARD', 'TRAFFIC OFFENSE', 'TRAFFIC STOP']
        drugs = ['DRUGS', 'OVERDOSE', 'DUI']"""

        for call in calls_list:
            g = call['geometry']['coordinates']
            p = call['properties']
            new_callid = int(p['CallID'])
            try:
                Calls.objects.get(callid=new_callid)
            except Calls.DoesNotExist:
                c = Calls()
                c.callid = new_callid
                c.lat, c.lon = g[0], g[1]
                c.geom = GEOSGeometry('POINT({:.6f} {:.6f})'.format(c.lat, c.lon), srid=4326)
                c.nature = p['Nature'].strip().upper()

                if c.nature not in call_natures:
                    call_natures.append(c.nature)
                try:
                    c.callgroup = lookup[c.nature]
                except:
                    c.callgroup = "NT"

                """if c.nature in propertycrime:
                    c.callgroup = 'PR'
                elif c.nature in violence:
                    c.callgroup = "VI"
                elif c.nature in accident:
                    c.callgroup = "AX"
                elif c.nature in traffic:
                    c.callgroup = "TR"
                elif c.nature in drugs:
                    c.callgroup = "DR" """

                c.callcategory = p['CallCategory'].strip().upper()
                c.address = p['Address'].strip()
                c.calldatetime = datetime.datetime.fromtimestamp(p['CallDateTime'] / 1000)
                if c.callgroup != "NT":
                    c.save()
                    feature_count += 1
        self.stdout.write('processed {} features'.format(feature_count))
        categoryfilename = datetime.datetime.today().strftime('%m%d%y') + 'categories'
        categoryfile = open(os.path.join(os.path.expanduser('~/Documents/'), categoryfilename), 'w')
        for cn in call_natures:
            categoryfile.write(cn)
            categoryfile.write(str('\n'))
        categoryfile.close()
