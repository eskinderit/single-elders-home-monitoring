#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 13:48:02 2022

@author: s
"""


import subprocess
import json
import csv

input_file = "./spline_boundary_enum.csv"      # examples file
condensed_examples = "condensed.csv"           # condensed examples file

# initialise condensed examples
# with initial examples from the examples file
n_examples = 50
g = open(input_file)
reader = csv.reader(g, delimiter=',')
f = open(condensed_examples, 'w', newline='')
writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for n in range(n_examples):
    ex = next(reader)
    coords = json.dumps([float(x) for x in ex[1:-1]])
    ex = [ex[0], coords, ex[-1]]
    writer.writerow(ex)
g.close()
f.close()

# ex_1 = next(reader)                            # read 2 examples
# ex_2 = next(reader)
# coords_1 = json.dumps([float(x) for x in ex_1[1:-1]])
# coords_2 = json.dumps([float(x) for x in ex_2[1:-1]])
# ex_1 = [ex_1[0], coords_1, ex_1[-1]]  # convert coords to json
# ex_2 = [ex_2[0], coords_2, ex_2[-1]]
# g.close()
# # print(ex_1)
# # print(ex_2)
# f = open(condensed_examples, 'w', newline='')
# writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# writer.writerow(ex_1)
# writer.writerow(ex_2)
# f.close()
last_condensed_size = n_examples
mapper_command = "'python3 ./mapper.py " + condensed_examples + "'"
out_dir = "./condensed_nearest_neighbour_classifier"
out_file = "part-00000"
step = True                                     # 1 -> true 0 -> false
while step:
# for n in range(4):
    subprocess.run(["rm", "-rf", out_dir])
    # with shell=True, a verbatim string instead of a sequence is recommended
    run_args = "$HADOOP_INSTALL/bin/hadoop jar $HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -files ./mapper.py,./reducer.py -mapper " + mapper_command + " -reducer ./reducer.py -input ./spline_boundary_enum.csv -output " + out_dir
    out = subprocess.run(run_args, stderr=subprocess.STDOUT, shell=True)
    subprocess.run("cat "+ out_dir + "/" + out_file + ">>"+ condensed_examples,
                   shell=True)
    f = open(condensed_examples)             # test the output for emptiness
    lines = f.readlines()
    f.close()
    # step = 0
    step = len(lines) != last_condensed_size      # same file -> stop repeating
    last_condensed_size = len(lines)