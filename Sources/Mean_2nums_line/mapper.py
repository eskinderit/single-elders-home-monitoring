#!/usr/bin/env python3
import sys

for line in sys.stdin:
  id_coords = line.split(',')  # CSV file
  line_sum = float(id_coords[1]) + float(id_coords[2])
  print('{0}\t{1}\t{2}'.format(0, line_sum, len(id_coords)-1))
