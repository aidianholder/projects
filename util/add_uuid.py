#! /usr/bin/env python

import uuid
import os
import csv

import psycopg2

conn = psycopg2.connect("dbname=projects user=admin")
cur = conn.cursor()

target = '~/Downloads/reports_all_test.csv'

with open(os.path.expanduser(target)) as csvfile:
    reader = csv.DictReader(csvfile)
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
        record['uuid'] = uuid.uuid5(uuid.NAMESPACE_DNS, row['name'] + row['address'])
        print record






