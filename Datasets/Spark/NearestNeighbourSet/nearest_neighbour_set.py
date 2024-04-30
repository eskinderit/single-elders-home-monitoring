from pyspark import SparkContext
import csv


def sq_sum(x):
  return sum((y ** 2 for y in x))

def sq_dist(x, y):
  return sq_sum((z[0] - z[1] for z in zip(x, y)))

def main():
   sc = SparkContext(appName='SparkNearestNeighbour')
   input_file = sc.textFile('/vagrant/Spark/NearestNeighbour/spline_boundary_enum_inputs.csv')
   nearest = input_file.map(lambda line: line.split(',')) \
                       .map(lambda pattern: [pattern[0], sq_dist((float(x) for x in pattern[1:]), (0,0))]) \
                       .reduce(lambda a, b: min(a, b, key=lambda k: k[-1]))
   f = open("nearest.csv", 'w')
   writer = csv.writer(f)
   writer.writerow(nearest)
   f.close()
   sc.stop()
if __name__ == '__main__':
   main()
