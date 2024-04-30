#!/usr/bin/env bash
$HADOOP_INSTALL/bin/hdfs dfs -rm -f -r ./variances  #dfs removes old results 
$HADOOP_INSTALL/bin/hadoop jar \
$HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-files ./mapper.py,./reducer.py \
-mapper ./mapper.py \
-reducer ./reducer.py \
-input ./data.csv -output ./variances  # input file in the DFS root