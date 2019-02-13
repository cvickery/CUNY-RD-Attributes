#! /usr/local/bin/python3
#
# generate a report of all course sections where the scheduled requirement designation and/or course
# attribute differs from the values in the CUNYfirst course catalog.
# NOTE: only the COPT attribute is checked.
#

import argparse
import csv
from collections import namedtuple

import psycopg2
from psycopg2.extras import NamedTupleCursor


parser = argparse.ArgumentParser(description='Generate report of RD/Attribute mismatches.')
parser.add_argument('term', type=int, help='CUNYfirst term number (CYYM)')
args = parser.parse_args()

conn = psycopg2.connect('dbname=cuny_courses')
cursor = conn.cursor(cursor_factory=NamedTupleCursor)

# Cache the course_attributes table
cursor.execute('select name, value from course_attributes')
attributes = dict()
for pair in cursor.fetchall():
  if pair[0] not in attributes.keys():
    attributes[pair[0]] = []
  attributes[pair[0]].append(pair[1])

# Process the scheduled-courses query
Record = None
with open(f'./queries/QNS_CV_CHECK_RD_ATTR-{args.term}.csv') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    if Record is None:
      row[0] = row[0].replace('\ufeff', '')
      cols = [col.lower().replace(' ', '_') for col in row]
      Record = namedtuple('Record', cols)
      continue
    else:
      record = Record._make(row)
      if record.crse_attr not in attributes.keys():
        print(f'Invalid crse_attr: {record.crse_attr} for {record.subject}, {record.catalog}')
      else:
        if record.crsatr_val not in attributes[record.crse_attr]:
          print('Invalid crsatr_val: {} for {} {} {}'.format(record.crsatr_val,
                                                             record.subject,
                                                             record.catalog,
                                                             record.crse_attr))
    cursor.execute("""
                    select  course_id,
                            offer_nbr,
                            department,
                            discipline,
                            catalog_number,
                            designation,
                            attributes
                      from  courses
                     where  course_id = %s
                       and  offer_nbr = %s
                  """, (int(record.course_id), int(record.offer_nbr)))
    if cursor.rowcount != 1:
      print(f'{record.course_id}, {record.offer_nbr} returned {cursor.rowcount} rows')
    else:
      course = cursor.fetchone()
      if record.crse_attr == 'COPT' and \
         f'{record.crse_attr}:{record.crsatr_val}' not in course.attributes:
        print(f'Attribute mismatch: section attribute “{record.crse_attr}:{record.crsatr_val}” ',
              end='')
        print(f'is not one of the course attributes, “{course.attributes}” for ', end='')
        print(f'{record.course_id}-{record.offer_nbr} {record.subject}, {record.catalog}; ', end='')
        print(f'section {record.section}')
      if record.designation != course.designation:
        print(f'Designation mismatch: section designation “{record.designation}” ', end='')
        print(f' is not the course designation, “{course.designation}” for ',
              end='')
        print(f'{record.course_id}-{record.offer_nbr} {record.subject}, {record.catalog}; ', end='')
        print(f'section {record.section}')
