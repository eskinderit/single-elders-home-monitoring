#!/usr/bin/env python3
import sys

tot_sum = 0
tot_num = 0

for line in sys.stdin:

  (_, num) = line.split('\t')
  tot_sum += float(num)
  tot_num += 1
  
print("%s" % (tot_sum/tot_num))
