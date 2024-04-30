# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 13:04:27 2022

@author: s
"""

import csv
import matplotlib.pyplot as plt
import random

with open('spline_boundary.csv') as f:
    reader = csv.reader(f, delimiter=',')
    reader.__next__()
    data = []                       # X Y dataset
    class1 = []                     # class 1 X
    class0 = []                     # class 2 X
    for x, y, c in reader:
        inp = [float(x), float(y)]  # convert inputs to float
        cl = int(c)                 # convert class to int
        data.append(inp + [cl])
        class1.append(inp) if cl else class0.append(inp)
    f.close()
# 2nd way
with open('spline_boundary.csv') as f:
    reader = csv.reader(f, delimiter=',')
    reader.__next__()
    xy_data = []                       # X Y dataset
    for e in reader:                # assume arbitrary dim
        inp = [float(x) for x in e[:-1]]  # convert inputs to float
        cl = int(e[-1])                   # convert class to int
        xy_data.append(inp + [cl])
    f.close()
first_class = list(filter(lambda xy: xy[-1], data))
second_class =list(filter(lambda xy: 1-xy[-1], data))

# save inputs as csv
# note newline='' in open, without it newlines are doubled
with open('spline_boundary_enum_inputs.csv', 'w', newline='') as f:  
    writer = csv.writer(f, delimiter=',')
    x_data = (x[:-1] for x in xy_data)
    en_inputs = [[i, *(data[i][:-1])] for i in range(len(data))]
    for x in en_inputs:
        writer.writerow(x)
f.close()
# plot classes for reference
p1 = plt.plot(*zip(*class1), '.', c='red')
p0 = plt.plot(*zip(*class0), '.', c='blue')
plt.savefig("spline_boundary.png", transparent=True)

# randomly generate a short sequence of points and classify them
n_queries = 100
with open('query_points.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    for i in range(n_queries):
        datum = random.random(), random.random()
        writer.writerow(datum)
f.close()

