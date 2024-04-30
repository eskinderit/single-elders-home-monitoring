from pyspark import SparkContext
def main():
   sc = SparkContext(appName='SparkWordCount')
   input_file = sc.textFile('/vagrant/Spark/WordCount/chaucer.txt')
   counts = input_file.flatMap(lambda line: line.split()) \
                     .map(lambda word: (word, 1)) \
                     .reduceByKey(lambda a, b: a + b)
   counts.saveAsTextFile('/vagrant/Spark/WordCount/output')
   sc.stop()
if __name__ == '__main__':
   main()
