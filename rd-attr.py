#! /usr/local/bin/python3
#
# generate a report of all course sections where the scheduled requirement designation and/or course
# attribute differe from the values in the CUNYfirst course catalog.

import argparse
import csv
from collections import namedtuple

parser = argparse.ArgumentParser(description='Generate report of RD/Attribute mismatches.')
parser.add_argument('term', type=int, help='CUNYfirst term number (CYYM)')
args = parser.parse_args()

Record = None
with open(f'./queries/QNS_CV_RD_ATTR-{args.term}.csv') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    if Record is None:
      row[0] = row[0].replace('\ufeff', '')
      cols = [col.lower().replace(' ', '_') for col in row]
      Record = namedtuple('Record', cols)
      continue
    else:
      record = Record._make(row)
      print(record)
      exit(0)
