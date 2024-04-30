#!/usr/bin/env python3
import sys

def sq_sum(x):
  return sum((y ** 2 for y in x))

def sq_dist(x, y):
  return sq_sum((z[0] - z[1] for z in zip(x, y)))

for line in sys.stdin:
  id_coords = line.split(',')  # CSV file
  id = int(id_coords[0])  # 1st field: point id
  # coordinates in the remaining fields
  coords = [float(c) for c in id_coords[1:]]
  # Generate the distance value
  sd = sq_dist(coords, (0, 0))
  print('{0}\t{1}'.format(id, sd))
