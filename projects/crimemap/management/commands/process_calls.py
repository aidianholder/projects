from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from ...models import Calls
from datetime import datetime, date, time
import os
from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
	help = 'process calls for service from spreadsheet in ../../data directory and loads them into database as Calls objects'

	def handle(self, *args, **options):
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
		try:
			f = open('/home/admin/src/projects/projects/crimemap/data/rplwisr.r3.csv', 'r')
			incidents = f.readlines()[2:-22]
			for incident in incidents:
				call = incident.split(',')
				new_callid = int(call[0][3:])
				try:
					Calls.objects.get(callid=new_callid)
				except Calls.DoesNotExist:
					c = Calls()
					c.callid = new_callid
					if call[4] != ' ':
						try:
							c.lat, c.lon = float(call[4])/1000000, float(call[5])/1000000
							c.geom = GEOSGeometry('POINT({:.6f} {:.6f})'.format(c.lon, c.lat), srid=4326)
						except ValueError:
							pass
					if call[2] != ' ':
						c.nature = call[2].strip().upper()
					try:
						c.callgroup = lookup[c.nature]
					except:
						c.callgroup = "NT"
					if call[3] != ' ':
						c.address = call[3].strip()
					date_time_raw = call[1].split()
					date_raw = date_time_raw[1].split('/')
					y = int(date_raw[2]) + 2000
					d = date(y, int(date_raw[0]), int(date_raw[1]))
					time_raw = date_time_raw[0].split(':')
					t = time(int(time_raw[0]), int(time_raw[1]), int(time_raw[2]))
					c.calldatetime = datetime.combine(d, t)
					if c.callgroup != "NT":
						try:
							c.save()
							feature_count +=1
						except:
							pass
			self.stdout.write('processed {} features'.format(feature_count))
			f.close()
			try:
				os.remove('/home/admin/src/projects/projects/crimemap/data/rplwisr.r3.csv')
			except OSError:
				self.stdout.write('file not found')
		except IOError:
			self.stdout.write('no file "rplwisr.r3.csv" present in crimemap/data dir')        
