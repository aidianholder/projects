#! /usr/bin/env python

import uuid
import os
import csv

import psycopg2
import psycopg2.extras

psycopg2.extras.register_uuid()

conn = psycopg2.connect("dbname=projects user=admin")
cur = conn.cursor()

target = '~/Downloads/reports_all_test.csv'

with open(os.path.expanduser(target)) as csvfile:
    reader = csv.DictReader(csvfile)
    uuid_list = []
    for row in reader:
        record = {}
        record['facility_name'] = row['name']
        record['facility_type'] = row['type']
        record['address'] = row['address']
        record['city'] = row['city']
        record['inspection_date'] = row['date']
        record['inspection_type'] = row['inspection']
        record['critical_points'] = row['critical']
        record['total_points'] = row['total']
        record['inspection_details'] = row['details']
        facility_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, row['name'] + row['address'])
        record['uuid'] = facility_uuid
        if facility_uuid not in uuid_list:
            cur.execute("""INSERT INTO inspections_facility (facility_name, facility_type, address, city, guid) VALUES (%(facility_name)s, %(facility_type)s, %(address)s, %(city)s, %(uuid)s)""", record)
        cur.execute("""INSERT INTO inspections_inspections (inspection_type, inspection_date, critical_points, total_points, inspection_details, facility_guid) VALUES (%(inspection_type)s, %(inspection_date)s, %(critical_points)s, %(total_points)s, %(inspection_details)s, %(uuid)s)""", record)
        conn.commit()
        uuid_list.append(facility_uuid)

        """print facility_uuid
        print type(facility_uuid)
        print type(record['uuid'])
        #if str(facility_uuid) not in uuid_list:"""

cur.close()
conn.close()

print uuid_list













