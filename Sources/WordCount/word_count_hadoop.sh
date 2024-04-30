#!/usr/bin/env bash

# cf. slide 36

rm -rf ./chaucer
$HADOOP_INSTALL/bin/hadoop jar \
$HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-files ./mapper.py,./reducer.py \
-mapper ./mapper.py \
-reducer ./reducer.py \
-input ./chaucer.txt -output ./chaucer
