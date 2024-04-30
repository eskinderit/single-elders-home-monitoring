#!/usr/bin/env python3
import sys

# reading a number for each line of input,
for line in sys.stdin:
  
  id_coords = line.split()
  
  # output read key, number 
  print('{0}\t{1}'.format(id_coords[0], float(id_coords[1])))
