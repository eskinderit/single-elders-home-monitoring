#!/usr/bin/env python3
import sys
import csv

def sq_sum(x):
  return sum((y ** 2 for y in x))

def sq_dist(x, y):
  return sq_sum((z[0] - z[1] for z in zip(x, y)))

query_file = str(sys.argv[1])  # name of query file
with open(query_file, newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  queries = []  # fill list with points in file
  for q in reader:
    queries.append([float(x) for x in q])
for line in sys.stdin:
  id_coords = line.split(',')
  id = int(id_coords[0])
  coords = [float(c) for c in id_coords[1:]]
  # Generate distance values for every query point
  q_id = 1
  for q in queries:
    sd = sq_dist(coords, q)
    print('{0}\t{1}\t{2}'.format(q_id, id, sd))
    q_id += 1
