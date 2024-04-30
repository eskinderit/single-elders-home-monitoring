#!/usr/bin/env python3
import sys
import csv

def sq_sum(x):
  return sum(y ** 2 for y in x)

def sq_dist(x, y):
  return sq_sum(u - v for u, v in zip(x, y))

query_file = str(sys.argv[1])  # name of query file
with open(query_file, newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  queries = []
  for q in reader:             # fill list with query points in file
    queries.append([float(x) for x in q])
for line in sys.stdin:
  id_coords_cl = line.split(',')
  id = int(id_coords_cl[0])                       # point identifier
  coords = [float(c) for c in id_coords_cl[1:-1]] # coordinate values
  cl_val = int(id_coords_cl[-1])                  # class value
  # Generate distance values for every query point
  q_id = 1
  for q in queries:
    sd = sq_dist(coords, q)
    print('%s\t%s\t%s\t%s' % (q_id, id, sd, cl_val))
    # print('{0}\t{1}\t{2}\t{3}'.format(q_id, id, sd, cl_val))
    q_id += 1
