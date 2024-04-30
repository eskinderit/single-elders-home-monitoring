#!/usr/bin/env python3

import sys
import math
(last_q_id, id_min, min_sd, cl_val) = (None, None, sys.maxsize, None)
for line in sys.stdin:
  # Get the id and squared distance from the current line
  (q_id, id, sd, cl_val) = line.split('\t')
  sd = float(sd)  # Convert the distance to a float
  if last_q_id and last_q_id != q_id:
    print("%s\t%s\t%s\t%s" % (last_q_id, id_min, math.sqrt(min_sd), nearest_cl_val))
    (last_q_id, id_min, min_sd, nearest_cl_val) = (q_id, id, sd, cl_val)
  else:
    if sd < min_sd:
      (last_q_id, id_min, min_sd, nearest_cl_val) = (q_id, id, sd, cl_val)
    elif sd == min_sd:
      (last_q_id, id_min, min_sd, nearest_cl_val) = \
          (q_id, min(id_min, id), min_sd, nearest_cl_val if id_min < id else cl_val)
print("%s\t%s\t%s\t%s" % (last_q_id, id_min, math.sqrt(min_sd), nearest_cl_val))
