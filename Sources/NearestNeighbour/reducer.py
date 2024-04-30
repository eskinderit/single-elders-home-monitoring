#!/usr/bin/env python3
import sys
import math
(last_id, min_sd) = (None, sys.maxsize)
# Process each key-value pair from the mapper
for line in sys.stdin:
  # Get the id and squared distance from the current line
  (id, sd) = line.split('\t')
  sd = float(sd)  # Convert the distance to a float
  if sd < min_sd:
    (last_id, min_sd) = (id, sd)
  elif sd == min_sd:
    (last_id, min_sd) = (min(last_id, id), min_sd)
print("%s\t%s" % (last_id, math.sqrt(min_sd)))
