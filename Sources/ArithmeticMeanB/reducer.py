#!/usr/bin/env python3
import sys

tot_sum = 0
tot_num = 0
curr_class = None

for line in sys.stdin:

  (class_, num) = line.split('\t')
  
  if not curr_class:
    curr_class = class_
  
  if class_ != curr_class:
    print(f"class: {curr_class}, mean: {tot_sum/tot_num}")
    curr_class = class_
    tot_sum = 0
    tot_num = 0
  
  
  tot_sum += float(num)
  tot_num += 1
  
print(f"class: {curr_class}, mean: {tot_sum/tot_num}")
