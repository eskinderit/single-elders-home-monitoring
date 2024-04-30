#!/usr/bin/env python3

import sys


line = next(sys.stdin)    # 1st line
last_id, last_coords, nst_e_id, nst_e_coords, min_sd, \
    last_cl_val, nst_e_cl_val = line.split('\t')
# print(line)
min_sd = float(min_sd)
for line in sys.stdin:
  # print(line)
  p_id, coords, e_id, e_coords, sd, cl_val, e_cl_val = \
        line.split('\t')  # get current line
  sd = float(sd)          # convert the distance to a float
  if last_id != p_id:       # point group ended
    # print([last_id, p_id])
    if int(last_cl_val) != int(nst_e_cl_val):  # incorrect prediction -> add example
      # print([last_id, p_id, last_cl_val, nst_e_cl_val])
      print("%s;%s;%s" % (last_id, last_coords, last_cl_val))
    last_id, last_coords, nst_e_id, nst_e_coords, min_sd, \
        last_cl_val, nst_e_cl_val = p_id, coords, e_id, e_coords, sd, cl_val, e_cl_val
  else:
    if sd < min_sd:
      nst_e_id, min_sd, nst_e_cl_val = e_id, sd, e_cl_val
    elif sd == min_sd:
      nst_e_id, nst_e_cl_val = min(nst_e_id, e_id), \
        nst_e_cl_val if nst_e_id < e_id else e_cl_val
if int(last_cl_val) != int(nst_e_cl_val):  # incorrect prediction -> add example
  print("%s;%s;%s" % (last_id, last_coords, last_cl_val))