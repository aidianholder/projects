#!/usr/bin/env python

import csv
import re
import uuid

import psycopg2
import psycopg2.extras

psycopg2.extras.register_uuid()

conn = psycopg2.connect("dbname=projects user=admin")
cur = conn.cursor()
cur.execute("""SELECT guid FROM inspections_facility""")
existing_guids = cur.fetchall()

guid_list = [str(guid[0]) for guid in existing_guids]

report = open('report.csv')

reader = csv.DictReader(report)

restaurants = []
record = {}
find_extra_spaces = re.compile('\s{2,}')

for row in reader:
    if row['facility_name'] != '':
        record = row
        fields = ['facility_name', 'facility_type', 'address', 'city']
        for field in fields:
            temp_value = row[field].strip()
            record[field] = find_extra_spaces.sub(' ', temp_value)
        facility_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, record['facility_name'] + record['address'])
        record['guid'] = str(facility_uuid)
    else:
        if record['inspection_date'] == '':
            record['inspection_date'] = row['inspection_date'].strip().replace("  ", " ")
            record['inspection'] = row['inspection'].strip().replace("  ", " ")
            record['results'] = row['results'].strip().strip().replace("  ", " ")
            if len(record) < 7:
                print len(record)
                print record
            restaurants.append(record)
        else:

            newrecord = record.copy()
            newrecord['inspection_date'] = row['inspection_date'].strip().replace("  ", " ")
            newrecord['inspection'] = row['inspection'].strip().replace("  ", " ")
            newrecord['results'] = row['results'].strip().replace("  ", " ")
            if len(record) < 7:
                print len(record)
                print record
            restaurants.append(newrecord)

cleanedrestaurants = []

find_scores = re.compile('\d+\/\d+')

for restaurant in restaurants:
    if restaurant['facility_type'] == 'Mobile':
        restaurant['address'] = ''
    if restaurant['inspection'] != 'Pre-Opening Inspection':
        if find_scores.match(restaurant['results']):
            scores = find_scores.match(restaurant['results']).group().split('/')
            restaurant['critical'] = scores[0]
            restaurant['total'] = scores[1]
            score_length = find_scores.match(restaurant['results']).end()
            restaurant['details'] = ''
            if len(restaurant['results']) > score_length:
                restaurant['details'] = restaurant['results'][score_length:]
        else:
            restaurant['critical'] = 0
            restaurant['total'] = 0
            restaurant['details'] = restaurant['results']
        cur.execute("""INSERT INTO inspections_inspections (inspection_type, inspection_date, critical_points, total_points, inspection_details, facility_guid_id ) VALUES (%(inspection)s, %(inspection_date)s, %(critical)s, %(total)s, %(details)s, %(guid)s)""", restaurant)
        if restaurant['guid'] not in guid_list:
            cur.execute("""INSERT INTO inspections_facility ( facility_name, facility_type, address, city, guid ) VALUES (%(facility_name)s, %(facility_type)s, %(address)s, %(city)s, %(guid)s)""", restaurant)
            guid_list.append(restaurant['guid'])
        conn.commit()

