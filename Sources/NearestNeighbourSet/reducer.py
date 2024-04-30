#!/usr/bin/env python3
import sys
import math
(last_q_id, id_min, min_sd) = (None, None, sys.maxsize)
for line in sys.stdin:
  # Get the id and squared distance from the current line
  (q_id, id, sd) = line.split('\t')
  sd = float(sd)  # Convert the distance to a float
  if last_q_id and last_q_id != q_id:
    print("%s\t%s\t%s" % (last_q_id, id_min, math.sqrt(min_sd)))
    (last_q_id, id_min, min_sd) = (q_id, id, sd)
  else:
    if sd < min_sd:
      (last_q_id, id_min, min_sd) = (q_id, id, sd)
    elif sd == min_sd:
      (last_q_id, id_min, min_sd) = (q_id, min(id_min, id), min_sd)
print("%s\t%s\t%s" % (last_q_id, id_min, math.sqrt(min_sd)))
