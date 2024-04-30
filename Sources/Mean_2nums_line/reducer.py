#!/usr/bin/env python3
import sys

tot_sum = 0
tot_num = 0

for line in sys.stdin:
  # Get the id and squared distance from the current line
  (_, sum, n_numbers) = line.split('\t')
  tot_sum += float(sum)
  tot_num += float(n_numbers)
  
print("%s" % (tot_sum/tot_num))
