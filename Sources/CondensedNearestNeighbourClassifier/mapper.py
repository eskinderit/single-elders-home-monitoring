#!/usr/bin/env python3
import sys
import csv
import json

def sq_sum(x):
  return sum(y ** 2 for y in x)

def sq_dist(x, y):
  return sq_sum(u - v for u, v in zip(x, y))

cons_file = str(sys.argv[1])     # name of condensed examples CSV file
with open(cons_file, newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=';')
  examples = []
  for e in reader:               # fill list with examples in file
    examples.append([int(e[0]), e[1], int(e[-1])])

for line in sys.stdin:
  id_coords_cl = line.split(',')
  p_id = int(id_coords_cl[0])                       # point identifier
  coords = [float(c) for c in id_coords_cl[1:-1]] # coordinate values
  cl_val = int(id_coords_cl[-1])                  # class value
  json_coords = json.dumps(coords)
  # Generate distance values for every query point
  for e in examples:
    sd = sq_dist(coords, json.loads(e[1]))
    print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format(p_id, json_coords, e[0], e[1],
                                          sd, cl_val, e[-1]))