#!/usr/bin/env python3
# we want to compute the variance for each column of the same group
import sys

line = next(sys.stdin)
inputs = line.split()   

# initialize key, count, coords 
last_key = inputs[0]
count = 1
coords = [float(i) for i in inputs[1:]]

for line in sys.stdin:

    inputs = line.split()
    
    key = inputs[0]
    nums = [float(i) for i in inputs[1:]]
    sq_nums = [float(i)**2 for i in inputs[1:]]
    
    if key == last_key:
        count += 1
        sum = [a + b for a,b in zip(coords, nums)]
        sq_sum = [a + b for a,b in zip(coords, sq_nums)]
    else:
        # output variance for values cumulated before
        print(last_key, end='\t')
        for i in range(len(nums)):
            print(sq_sum[i]/count - (sum[i]/count)**2, end=' ')
        print(end='\n')
    
        # re-initialize values for a group with a different key
        last_key = inputs[0]
        count = 1
        coords = [float(i) for i in inputs[1:]]    

# print last key variances
print(last_key, end='\t')
for i in range(len(nums)):
    print(sq_sum[i]/count - (sum[i]/count)**2, end=' ')
print(end='\n')
    
    
