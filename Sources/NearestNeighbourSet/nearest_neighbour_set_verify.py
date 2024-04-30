import matplotlib.pyplot as plt
import csv


with open("../../Datasets/spline_boundary.csv") as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    data = [[float(x) for x in xy[:-1]] for xy in reader ]
f.close()
with open("../../Datasets/query_points.csv") as f:
    reader = csv.reader(f, delimiter=',')
    queries = [[float(x) for x in q] for q in reader ]
f.close()
# open Hadoop results
with open("nearest_neighbour_set/part-00000") as f:
    reader = csv.reader(f, delimiter='\t')
    neighbours = [data[int(a[1])] for a in reader]
f.close()
# 
# plot data, queries, neighbours
fig, axs = plt.subplots()
axs.set_aspect('equal', 'box')
axs.plot(*zip(*data), '.', c='blue', )
axs.plot(*zip(*queries), '+', c='red')
axs.plot(*zip(*neighbours), '*', c='cyan')
fig.savefig("nearest_neighbours_set_verify.png", transparent=True)